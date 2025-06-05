import torch
import cv2
import numpy as np
import platform

from pathlib import PosixPath

import base64
import io
from PIL import Image

import sys

# macOS에서만 WindowsPath → PosixPath 패치
def patch_windows_path_loader():
    import pathlib
    from unittest.mock import patch

    class DummyWindowsPath(type(pathlib.Path())):
        def __new__(cls, *args, **kwargs):
            return PosixPath(*args, **kwargs)

    patcher = patch("pathlib.WindowsPath", DummyWindowsPath)
    patcher.start()
    return patcher

class Generator:
    def __init__(self):
        # OS가 macOS일 경우에만 패치 적용
        if platform.system() == "Darwin":
            patch = patch_windows_path_loader()

        # 학습된 모델의 가중치 파일 경로
        self.weights_path = 'weights/best.pt'  # 또는 'last.pt'

        # YOLOv5 모델 불러오기
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=self.weights_path)

    def generate(self, pil_image: Image.Image):
        # PIL → numpy array → BGR 변환
        img = np.array(pil_image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # 예측 수행
        results = self.model(img)

        # 결과 이미지 시각화
        results.render()  # results.imgs에 결과 이미지 저장됨

        # BGR → RGB → PIL
        rendered_img = Image.fromarray(cv2.cvtColor(results.ims[0], cv2.COLOR_BGR2RGB))

        # PIL → base64
        buffered = io.BytesIO()
        rendered_img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return img_base64

