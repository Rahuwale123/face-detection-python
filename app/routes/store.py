import io
import json
import face_recognition
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from app.database import get_connection
from app.face_utils import encode_face_from_image_bytes

store_router = APIRouter()

@store_router.post("/store_employees/")
async def upload_face(
    image: UploadFile = File(...),
    name: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    department: str = Form("Unknown"),
    village:str=Form(...)
):
    try:
        # Read image bytes
        image_bytes = await image.read()
        image_data = face_recognition.load_image_file(io.BytesIO(image_bytes))
        face_encodings = face_recognition.face_encodings(image_data)

        if not face_encodings:
            raise HTTPException(status_code=400, detail="No face detected in the image")

        face_encoding_json = json.dumps(face_encodings[0].tolist())

        conn = get_connection()
        cursor = conn.cursor()

        # Check for duplicate user_id
        cursor.execute("SELECT COUNT(*) FROM Profile_details WHERE user_id = %s", (user_id,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail=f"user_id {user_id} already exists")

        # Insert into DB
        cursor.execute(
            "INSERT INTO profile_details (name, user_id, department, face_encoding, village) VALUES (%s, %s, %s, %s,%s)",
            (name, user_id, department, face_encoding_json,village)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return JSONResponse(content={"message": "Face data stored successfully"}, status_code=200)

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))