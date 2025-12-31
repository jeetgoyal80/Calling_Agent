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
    priority = calculate_priority(intent_data)

    os.makedirs(os.path.dirname(COMPLAINT_FILE), exist_ok=True)

    if os.path.exists(COMPLAINT_FILE):
        with open(COMPLAINT_FILE, "r", encoding="utf-8") as f:
            try:
                complaints = json.load(f)
            except json.JSONDecodeError:
                complaints = []
    else:
        complaints = []

    # 🔁 DUPLICATE CHECK
    duplicate = find_duplicate_complaint(student, intent_data, complaints)
    if duplicate:
        return duplicate["complaint_id"], True   # True = duplicate

    # ✅ NEW COMPLAINT
    complaint = {
        "complaint_id": str(uuid.uuid4())[:8],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "student": {
            "scholar_no": student.get("scholar_no", ""),
            "name": student["name"],
            "branch": student["branch"],
            "year": student.get("year", "")
        },
        "location": {
            "hostel": student.get("hostel"),
            "room": student.get("room")
        },
        "department": "Hostel Maintenance",
        "issue": {
            "type": intent_data.get("issue_type"),
            "severity": intent_data.get("severity")
        },
        "priority": priority,
        "complaint_text": raw_text,
        "status": "OPEN"
    }

    complaints.append(complaint)

    with open(COMPLAINT_FILE, "w", encoding="utf-8") as f:
        json.dump(complaints, f, indent=4)

    return complaint["complaint_id"], False   # False = new complaint

def calculate_priority(intent_data):
    issue_type = intent_data.get("issue_type")
    severity = intent_data.get("severity")

    if issue_type == "water":
        return "HIGH"

    if issue_type == "light" and severity == "not_working":
        return "HIGH"

    if issue_type == "fan" and severity == "not_working":
        return "MEDIUM"

    if severity == "fluctuating":
        return "LOW"

    return "MEDIUM"


def find_duplicate_complaint(student, intent_data, complaints):
    for c in complaints:
        if (
            c["status"] == "OPEN"
            and c["location"]["hostel"] == student.get("hostel")
            and c["location"]["room"] == student.get("room")
            and c["issue"]["type"] == intent_data.get("issue_type")
        ):
            return c
    return None

