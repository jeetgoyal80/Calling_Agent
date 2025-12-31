import json
from datetime import datetime
import uuid
import os





COMPLAINT_FILE = "complaints/complaints.json"

def load_students():
    with open("db/students.json", "r", encoding="utf-8") as f:
        return json.load(f)

def solve_hostel_issue(student, intent_data):
    issue_type = intent_data.get("issue_type")
    location = intent_data.get("location")

    if issue_type == "light":
        return (
            f"{student['name']}, your room light complaint has been registered. "
            "Maintenance team will resolve it within 24 to 48 hours."
        )

    if issue_type == "fan":
        return (
            f"{student['name']}, your room fan issue has been registered. "
            "Maintenance team will check it soon."
        )

    if issue_type == "water":
        return (
            f"{student['name']}, your water supply complaint has been registered. "
            "Maintenance team will take action shortly."
        )

    return None


def save_complaint(student, intent_data, raw_text):
    print("[DEBUG] save_complaint() called")

    complaint = {
        "complaint_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student": {
            "scholar_no": student.get("scholar_no", ""),
            "name": student["name"],
            "branch": student["branch"],
            "year": student.get("year", ""),
        },
        "location": {
            "hostel": student.get("hostel", ""),
            "room": student.get("room", "")
        },
        "department": "Hostel Maintenance",
        "issue": {
            "type": intent_data.get("issue_type"),
            "severity": intent_data.get("severity")
        },
        "complaint_text": raw_text,
        "status": "OPEN"
    }

    os.makedirs(os.path.dirname(COMPLAINT_FILE), exist_ok=True)

    if os.path.exists(COMPLAINT_FILE):
        with open(COMPLAINT_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(complaint)

    with open(COMPLAINT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("[DEBUG] Complaint saved:", complaint["complaint_id"])
    return complaint["complaint_id"]
