from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from PIL import Image, ImageOps


def read_image_to_cv(image_bytes: bytes) -> np.ndarray:
    image = np.asarray(bytearray(image_bytes), dtype=np.uint8)
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


def detect_primary_face(image: np.ndarray) -> Tuple[int, int, int, int]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(80, 80))
    if len(faces) == 0:
        h, w, _ = image.shape
        size = min(h, w)
        offset_x = (w - size) // 2
        offset_y = int(h * 0.15)
        return offset_x, offset_y, size, size

    # pick the largest face
    x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
    padding = int(max(w, h) * 0.25)
    x = max(x - padding, 0)
    y = max(y - padding, 0)
    w = min(w + padding * 2, image.shape[1] - x)
    h = min(h + padding * 2, image.shape[0] - y)
    return x, y, w, h


def crop_align_face(image_bytes: bytes, size: int = 512) -> Image.Image:
    image = read_image_to_cv(image_bytes)
    x, y, w, h = detect_primary_face(image)
    cropped = image[y : y + h, x : x + w]
    pil_image = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
    pil_image = ImageOps.fit(pil_image, (size, size), method=Image.Resampling.LANCZOS)
    return pil_image


def save_face(image: Image.Image, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG")


def transparent_background(image: Image.Image) -> Image.Image:
    # quick background cleanup via mask of dominant color
    image = image.convert("RGBA")
    data = np.array(image)
    rgb_data = data[:, :, :3].reshape(-1, 3)
    dominant = np.median(rgb_data, axis=0)
    distance = np.linalg.norm(rgb_data - dominant, axis=1)
    threshold = np.percentile(distance, 60)
    alpha_mask = (distance > threshold).astype(np.uint8) * 255
    alpha_mask = alpha_mask.reshape(data.shape[:2])
    data[:, :, 3] = alpha_mask
    return Image.fromarray(data)

