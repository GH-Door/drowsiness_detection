import urllib.request
import cv2
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

# pose_landmarker.task 모델 자동 다운로드
_MODEL_PATH = Path(__file__).parent / "pose_landmarker_lite.task"
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
)


def _ensure_model() -> str:
    if not _MODEL_PATH.exists():
        print(f"모델 다운로드 중: {_MODEL_URL}")
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print(f"저장 완료: {_MODEL_PATH}")
    return str(_MODEL_PATH)


@dataclass
class PoseResult:
    """포즈 검출 결과"""
    head_down: bool        # 고개 숙임 여부 (pitch 추정)
    landmarks: np.ndarray  # (33, 3) 정규화 좌표


class PoseDetector:
    """
    MediaPipe PoseLandmarker(Tasks API) 기반 자세 검출기.
    Face Landmarker가 실패할 때 fallback으로 사용.
    고개 숙임 여부를 어깨-코 랜드마크 기반으로 추정.
    """

    # MediaPipe Pose 랜드마크 인덱스
    _NOSE = 0
    _LEFT_SHOULDER = 11
    _RIGHT_SHOULDER = 12

    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        head_down_threshold: float = 0.15,
    ):
        """
        Args:
            min_detection_confidence: 포즈 검출 최소 신뢰도
            head_down_threshold: 코가 어깨 중심보다 이 값 이상 아래이면 고개 숙임으로 판단
                                  (정규화 좌표 기준, 0.0~1.0)
        """
        self._threshold = head_down_threshold
        options = vision.PoseLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=_ensure_model()),
            num_poses=1,
            min_pose_detection_confidence=min_detection_confidence,
            running_mode=vision.RunningMode.IMAGE,
        )
        self._detector = vision.PoseLandmarker.create_from_options(options)

    def detect(self, image: np.ndarray) -> Optional[PoseResult]:
        """
        이미지에서 포즈를 검출합니다.

        Args:
            image: BGR numpy 배열

        Returns:
            PoseResult (검출 성공) 또는 None (검출 실패)
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = self._detector.detect(mp_image)

        if not result.pose_landmarks:
            return None

        lm = result.pose_landmarks[0]
        landmarks = np.array([[p.x, p.y, p.z] for p in lm], dtype=np.float32)

        nose_y = landmarks[self._NOSE, 1]
        shoulder_y = (landmarks[self._LEFT_SHOULDER, 1] + landmarks[self._RIGHT_SHOULDER, 1]) / 2
        head_down = bool((nose_y - shoulder_y) > -self._threshold)

        return PoseResult(head_down=head_down, landmarks=landmarks)

    def close(self):
        self._detector.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
