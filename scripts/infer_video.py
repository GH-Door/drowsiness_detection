"""
영상 파일 추론 스크립트.

실행:
    uv run python scripts/infer_video.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional
from ultralytics import YOLO

from src.models.yolo_trainer import predict
from src.detection.face import FaceDetector
from src.detection.metrics import mean_ear, mar, head_pose
from src.detection.temporal import FrameResult, TemporalAnalyzer, TemporalState


@dataclass
class PipelineConfig:
    """
    StudentPipeline 설정.
    각 기능을 on/off하거나 임계값을 조정할 수 있음.

    Args:
        yolo_conf: YOLO 탐지 신뢰도 임계값
        face_conf: MediaPipe Face 검출 신뢰도 임계값
        brighten_crop: YOLO crop에 밝기 보정 적용 여부
        brighten_alpha: 밝기 보정 대비 (1.0~2.0)
        brighten_beta: 밝기 보정 밝기 (0~100)
        use_pose_fallback: face_detected=False 시 Pose로 고개 숙임 감지
        pose_conf: MediaPipe Pose 검출 신뢰도 임계값
        ear_threshold: EAR 졸음 임계값
        ear_consec_frames: EAR 연속 프레임 수
        mar_threshold: MAR 하품 임계값
        mar_consec_frames: MAR 연속 프레임 수
        departed_sec: 이탈 판단 지속 초
        fps: 영상 FPS
    """
    yolo_conf: float = 0.4
    face_conf: float = 0.2
    brighten_crop: bool = True
    brighten_alpha: float = 1.5
    brighten_beta: float = 30.0
    use_pose_fallback: bool = False
    pose_conf: float = 0.5
    ear_threshold: float = 0.20
    ear_consec_frames: int = 15
    mar_threshold: float = 0.50
    mar_consec_frames: int = 3
    departed_sec: float = 5.0
    fps: float = 30.0


class StudentPipeline:
    """
    수강생 단위 졸음/이탈 감지 파이프라인.

    YOLO → Face Landmarker → (Pose Fallback) → Temporal 분석

    사용 예시:
        config = PipelineConfig(use_pose_fallback=True, ear_threshold=0.18)
        pipeline = StudentPipeline(yolo_model, config)

        with pipeline:
            for frame in frames:
                results = pipeline.process_frame(frame)
                for r in results:
                    print(r["temporal"].state)
    """

    def __init__(self, yolo_model, config: Optional[PipelineConfig] = None):
        self._model = yolo_model
        self._cfg = config or PipelineConfig()
        self._face_detector: Optional[FaceDetector] = None
        self._pose_detector = None
        self._analyzers: dict[str, TemporalAnalyzer] = {}

    def _get_analyzer(self, bbox_key: str) -> TemporalAnalyzer:
        if bbox_key not in self._analyzers:
            self._analyzers[bbox_key] = TemporalAnalyzer(
                fps=self._cfg.fps,
                ear_threshold=self._cfg.ear_threshold,
                ear_consec_frames=self._cfg.ear_consec_frames,
                mar_threshold=self._cfg.mar_threshold,
                mar_consec_frames=self._cfg.mar_consec_frames,
                departed_sec=self._cfg.departed_sec,
                use_pose_fallback=self._cfg.use_pose_fallback,
            )
        return self._analyzers[bbox_key]

    def process_frame(self, frame: np.ndarray) -> list[dict]:
        detections = predict(self._model, frame, conf=self._cfg.yolo_conf)
        outputs = []

        for det in detections:
            x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
            bbox_key = f"{x1}_{y1}_{x2}_{y2}"

            frame_result = FrameResult(yolo_class=det["class_name"])
            face_result = None

            if det["class_name"] == "person_on":
                crop = frame[y1:y2, x1:x2]

                if self._cfg.brighten_crop:
                    crop = cv2.convertScaleAbs(
                        crop,
                        alpha=self._cfg.brighten_alpha,
                        beta=self._cfg.brighten_beta,
                    )

                face_result = self._face_detector.detect(crop)

                if face_result is not None:
                    frame_result.face_detected = True
                    frame_result.ear = float(mean_ear(face_result.landmarks_px))
                    frame_result.mar = float(mar(face_result.landmarks_px))
                    p, y = head_pose(face_result.landmarks)
                    frame_result.pitch = float(p)
                    frame_result.yaw = float(y)

                elif self._cfg.use_pose_fallback and self._pose_detector is not None:
                    pose_result = self._pose_detector.detect(crop)
                    if pose_result is not None:
                        frame_result.pose_head_down = pose_result.head_down

            analyzer = self._get_analyzer(bbox_key)
            temporal = analyzer.update(frame_result)

            outputs.append({
                "bbox": det["bbox"],
                "yolo_class": det["class_name"],
                "yolo_conf": round(det["confidence"], 3),
                "face_detected": frame_result.face_detected,
                "landmarks_px": face_result.landmarks_px if face_result is not None else None,
                "ear": round(frame_result.ear, 3) if frame_result.ear is not None else None,
                "mar": round(frame_result.mar, 3) if frame_result.mar is not None else None,
                "pitch": round(frame_result.pitch, 1) if frame_result.pitch is not None else None,
                "yaw": round(frame_result.yaw, 1) if frame_result.yaw is not None else None,
                "pose_head_down": frame_result.pose_head_down,
                "temporal": temporal,
            })

        return outputs

    def open(self):
        self._face_detector = FaceDetector(min_detection_confidence=self._cfg.face_conf)
        if self._cfg.use_pose_fallback:
            from src.detection.pose import PoseDetector
            self._pose_detector = PoseDetector(min_detection_confidence=self._cfg.pose_conf)
        return self

    def close(self):
        if self._face_detector:
            self._face_detector.close()
        if self._pose_detector:
            self._pose_detector.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, *_):
        self.close()


if __name__ == "__main__":
    from src.utils.loaders import load_env
    load_env()

    CHECKPOINT = Path("checkpoint/yolo11n/weights/best.pt")
    VIDEO_PATH = Path("data/video/TestVideo2.mp4")
    OUTPUT_PATH = Path("data/video/output.mp4")

    yolo_model = YOLO(str(CHECKPOINT))
    config = PipelineConfig(
        use_pose_fallback=False,  # Pose fallback 사용 여부
    )

    cap = cv2.VideoCapture(str(VIDEO_PATH))
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    config.fps = fps

    out = cv2.VideoWriter(str(OUTPUT_PATH), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    CLASS_COLORS = {"person_on": (0, 255, 0), "person_off": (0, 0, 255), "screen_off": (128, 128, 128)}
    STATE_COLORS = {"normal": (0, 255, 0), "drowsy": (0, 0, 255), "yawn": (0, 165, 255), "departed": (128, 128, 128)}

    with StudentPipeline(yolo_model, config) as pipeline:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            results = pipeline.process_frame(frame)

            for r in results:
                x1, y1, x2, y2 = [int(v) for v in r["bbox"]]
                color = CLASS_COLORS.get(r["yolo_class"], (255, 255, 255))
                state = r["temporal"].state.value
                state_color = STATE_COLORS.get(state, (255, 255, 255))

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{r['yolo_class']} {r['yolo_conf']:.2f}",
                            (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
                cv2.putText(frame, f"[{state}]",
                            (x1, y2 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, state_color, 1)

                if r["ear"] is not None:
                    cv2.putText(frame, f"EAR:{r['ear']:.2f}",
                                (x2 + 5, y1 + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                    cv2.putText(frame, f"P:{r['pitch']:.0f} Y:{r['yaw']:.0f}",
                                (x2 + 5, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

            out.write(frame)

    cap.release()
    out.release()
    print(f"저장 완료: {OUTPUT_PATH}")
