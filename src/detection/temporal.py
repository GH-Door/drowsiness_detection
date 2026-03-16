from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class State(Enum):
    NORMAL     = "normal"
    DROWSY     = "drowsy"
    YAWN       = "yawn"
    DEPARTED   = "departed"
    SCREEN_OFF = "screen_off"


@dataclass
class FrameResult:
    """
    파이프라인 한 프레임의 결과.
    StudentPipeline → TemporalAnalyzer로 전달되는 단위.
    """
    yolo_class: Optional[str]    # "person_on" | "person_off" | "screen_off" | None
    face_detected: bool = False
    ear: Optional[float] = None
    mar: Optional[float] = None
    pitch: Optional[float] = None
    yaw: Optional[float] = None
    pose_head_down: Optional[bool] = None  # Pose fallback 결과


@dataclass
class TemporalState:
    """TemporalAnalyzer가 반환하는 현재 상태"""
    state: State
    ear: Optional[float] = None
    mar: Optional[float] = None
    pitch: Optional[float] = None
    yaw: Optional[float] = None
    drowsy_frames: int = 0
    yawn_frames: int = 0
    departed_frames: int = 0


class TemporalAnalyzer:
    """
    프레임 단위 결과를 시간 윈도우로 누적해 졸음/하품/이탈 상태를 판단.

    Args:
        fps: 영상 FPS (프레임→초 변환에 사용)
        ear_threshold: EAR이 이 값 이하이면 졸음 의심 (기본 0.20)
        ear_consec_frames: 연속 졸음 의심 프레임 수 (기본 15 → ~0.5초 @ 30fps)
        mar_threshold: MAR이 이 값 이상이면 하품 의심 (기본 0.50)
        mar_consec_frames: 연속 하품 의심 프레임 수 (기본 3)
        departed_sec: person_off / screen_off 지속 초 수 (기본 5초)
        use_pose_fallback: Pose 기반 고개 숙임 감지 사용 여부
        pose_consec_frames: 고개 숙임 연속 프레임 수 (기본 20)
    """

    def __init__(
        self,
        fps: float = 30.0,
        ear_threshold: float = 0.20,
        ear_consec_frames: int = 15,
        mar_threshold: float = 0.50,
        mar_consec_frames: int = 3,
        departed_sec: float = 5.0,
        use_pose_fallback: bool = False,
        pose_consec_frames: int = 20,
    ):
        self._fps = fps
        self._ear_threshold = ear_threshold
        self._ear_consec = ear_consec_frames
        self._mar_threshold = mar_threshold
        self._mar_consec = mar_consec_frames
        self._departed_frames = int(departed_sec * fps)
        self._use_pose = use_pose_fallback
        self._pose_consec = pose_consec_frames

        self._ear_counter = 0
        self._mar_counter = 0
        self._depart_counter = 0
        self._pose_counter = 0

    def update(self, result: FrameResult) -> TemporalState:
        """
        프레임 결과 하나를 받아 현재 상태를 반환.

        Args:
            result: FrameResult (파이프라인에서 생성)

        Returns:
            TemporalState
        """
        # screen_off → 즉시 SCREEN_OFF 반환
        if result.yolo_class == "screen_off":
            self._depart_counter = 0
            self._ear_counter = 0
            self._mar_counter = 0
            self._pose_counter = 0
            return TemporalState(state=State.SCREEN_OFF)

        # 이탈 카운터 (person_off만 해당)
        if result.yolo_class == "person_off":
            self._depart_counter += 1
            self._ear_counter = 0
            self._mar_counter = 0
            self._pose_counter = 0
        else:
            self._depart_counter = 0

        if self._depart_counter >= self._departed_frames:
            return TemporalState(state=State.DEPARTED, departed_frames=self._depart_counter)

        # EAR 졸음 카운터
        if result.face_detected and result.ear is not None:
            if result.ear < self._ear_threshold:
                self._ear_counter += 1
            else:
                self._ear_counter = 0
        else:
            self._ear_counter = 0

        # MAR 하품 카운터
        if result.face_detected and result.mar is not None:
            if result.mar > self._mar_threshold:
                self._mar_counter += 1
            else:
                self._mar_counter = 0
        else:
            self._mar_counter = 0

        # Pose fallback 카운터
        if self._use_pose and not result.face_detected and result.pose_head_down:
            self._pose_counter += 1
        else:
            self._pose_counter = 0

        # 상태 판단 (우선순위: DROWSY > YAWN > NORMAL)
        if self._ear_counter >= self._ear_consec:
            state = State.DROWSY
        elif self._use_pose and self._pose_counter >= self._pose_consec:
            state = State.DROWSY
        elif self._mar_counter >= self._mar_consec:
            state = State.YAWN
        else:
            state = State.NORMAL

        return TemporalState(
            state=state,
            ear=result.ear,
            mar=result.mar,
            pitch=result.pitch,
            yaw=result.yaw,
            drowsy_frames=self._ear_counter,
            yawn_frames=self._mar_counter,
        )

    def reset(self):
        """카운터 초기화 (수강생 전환 시 사용)"""
        self._ear_counter = 0
        self._mar_counter = 0
        self._depart_counter = 0
        self._pose_counter = 0
