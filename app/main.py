from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from app.video_processor import process_video
from app.models import SessionLocal, VideoEvent
import os

app = FastAPI()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_path = f"test_videos/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    output_path = process_video(file_path, file.filename)
    return FileResponse(output_path)

@app.get("/timeline/{filename}")
def get_timeline(filename: str):
    db = SessionLocal()
    events = db.query(VideoEvent).filter(VideoEvent.filename == filename).all()
    result = [{"timestamp": e.timestamp, "position": e.position} for e in events]
    db.close()
    return JSONResponse(content=result)