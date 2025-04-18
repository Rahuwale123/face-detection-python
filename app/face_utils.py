import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO

def encode_face_from_image_bytes(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image, dtype=np.uint8)
    encodings = face_recognition.face_encodings(image_np)
    return encodings[0] if encodings else None
