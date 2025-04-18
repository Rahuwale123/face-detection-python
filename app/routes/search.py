import json
import numpy as np
import face_recognition
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.database import get_connection
from app.face_utils import encode_face_from_image_bytes

search_router = APIRouter()

@search_router.post("/search_employee/")
async def search_employee(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        uploaded_encoding = encode_face_from_image_bytes(image_bytes)

        if uploaded_encoding is None:
            raise HTTPException(status_code=400, detail="No face detected in uploaded image.")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, user_id, department, face_encoding, village FROM Profile_details")
        Profile_details = cursor.fetchall()
        cursor.close()
        conn.close()

        for name, user_id, department, stored_encoding_json, village in Profile_details:
            stored_encoding = np.array(json.loads(stored_encoding_json))
            match = face_recognition.compare_faces([stored_encoding], uploaded_encoding, tolerance=0.5)

            if match[0]:
                return {
                    "message": "Employee Found",
                    "name": name,
                    "user_id": user_id,
                    "department": department,
                    'Village':village
                }

        return {"message": "Employee not found"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
