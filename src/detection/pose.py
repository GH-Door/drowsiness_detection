import cv2
import numpy as np
from dataclasses import dataclass
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision


@dataclass
class PoseResult:
    """포즈 검출 결과"""
    head_down: bool       # 고개 숙임 여부 (pitch 추정)
    landmarks: np.ndarray # (33, 3) 정규화 좌표


class PoseDetector:
    """
    MediaPipe Pose 기반 자세 검출기.
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
        min_tracking_confidence: float = 0.5,
        head_down_threshold: float = 0.15,
    ):
        """
        Args:
            min_detection_confidence: 포즈 검출 최소 신뢰도
            min_tracking_confidence: 포즈 추적 최소 신뢰도
            head_down_threshold: 코가 어깨 중심보다 이 값 이상 아래이면 고개 숙임으로 판단
                                  (정규화 좌표 기준, 0.0~1.0)
        """
        self._threshold = head_down_threshold
        self._pose = mp.solutions.pose.Pose(
            static_image_mode=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, image: np.ndarray) -> Optional[PoseResult]:
        """
        이미지에서 포즈를 검출합니다.

        Args:
            image: BGR numpy 배열

        Returns:
            PoseResult (검출 성공) 또는 None (검출 실패)
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self._pose.process(rgb)

        if not result.pose_landmarks:
            return None

        lm = result.pose_landmarks.landmark
        landmarks = np.array([[p.x, p.y, p.z] for p in lm], dtype=np.float32)

        nose_y = landmarks[self._NOSE, 1]
        shoulder_y = (landmarks[self._LEFT_SHOULDER, 1] + landmarks[self._RIGHT_SHOULDER, 1]) / 2
        head_down = bool((nose_y - shoulder_y) > -self._threshold)

        return PoseResult(head_down=head_down, landmarks=landmarks)

    def close(self):
        self._pose.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
