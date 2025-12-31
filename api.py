from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import uuid
import os

from stt import speech_to_text
from intent import detect_intent
from state_machine import (
    load_students,
    solve_hostel_issue,
    save_complaint
)

app = FastAPI(title="MANIT Voice Helpdesk")

students = load_students()

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


@app.post("/process-audio")
async def process_audio(
    scholar_no: str,
    audio: UploadFile = File(...)
):
    audio_path = f"{AUDIO_DIR}/{uuid.uuid4()}.wav"

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)

    try:
        # ---- VERIFY STUDENT ----
        if scholar_no not in students:
            return JSONResponse(
                status_code=400,
                content={"error": "Invalid scholar number"}
            )

        student = students[scholar_no]

        # ---- STT ----
        issue_text = speech_to_text(audio_path)

        # ---- INTENT ----
        intent_data = detect_intent(issue_text)

        if intent_data.get("intent") != "hostel":
            return {
                "status": "unsupported",
                "message": "Issue cannot be handled automatically"
            }

        # ---- COMPLAINT ----
        response = solve_hostel_issue(student, intent_data)

        complaint_id, is_duplicate = save_complaint(
            student=student,
            intent_data=intent_data,
            raw_text=issue_text
        )

        return {
            "status": "ok",
            "duplicate": is_duplicate,
            "complaint_id": complaint_id,
            "message": response,
            "parsed_issue": intent_data,
            "transcript": issue_text
        }

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)