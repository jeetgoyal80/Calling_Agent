import winsound
from stt import speech_to_text, extract_digits
from tts import speak
from intent import detect_intent
from state_machine import load_students, solve_hostel_issue, save_complaint

students = load_students()

MAX_DIGITS = 10
MAX_ATTEMPTS = 3


# ---------- BEEP ----------
def beep():
    winsound.Beep(1000, 400)


# ---------- GREETING ----------
speak("Namaskar.")
speak("You are connected to MANIT helpdesk.")
speak("Beep ke baad apna scholar number boliye.")
beep()


# ---------- SCHOLAR NUMBER ----------
attempts = 0
collected_digits = ""
student = None

while attempts < MAX_ATTEMPTS:
    print("\n[System] Waiting for scholar number...")

    spoken_text = speech_to_text()
    digits = extract_digits(spoken_text)

    print("[System] Extracted digits:", digits)

    if not digits:
        speak("Main aapka scholar number nahi sun paaya. Please dobara try kijiye.")
        beep()
        attempts += 1
        continue

    collected_digits += digits
    print("[System] Collected so far:", collected_digits)

    if len(collected_digits) >= MAX_DIGITS:
        candidate = collected_digits[-MAX_DIGITS:]
        print("[System] Candidate scholar number:", candidate)

        if candidate in students:
            student = students[candidate]
            break
        else:
            speak("Scholar number galat lag raha hai. Please poora number dobara boliye.")
            collected_digits = ""
            beep()
            attempts += 1
    else:
        speak("Number incomplete hai. Please remaining digits boliye.")
        beep()


# ---------- FAILED VERIFICATION ----------
if not student:
    speak(
        "Aapki identity verify nahi ho paayi. "
        "Please helpdesk office se directly contact kijiye."
    )
    exit()


# ---------- STUDENT VERIFIED ----------
speak(f"Hello {student['name']}.")
speak(f"Aap {student['branch']} branch se hain.")
speak("Beep ke baad apni problem bataiye.")
beep()

print("\n[System] Waiting for student problem...")


# ---------- PROBLEM ----------
issue_text = speech_to_text()

intent_data = detect_intent(issue_text)
print("[System] Detected intent:", intent_data)


if intent_data.get("intent") == "hostel":

    response = solve_hostel_issue(student, intent_data)

    if response:
        complaint_id, is_duplicate = save_complaint(
            student=student,
            intent_data=intent_data,
            raw_text=issue_text
        )

        if is_duplicate:
            speak(
                f"{student['name']}, is room ke liye pehle se complaint register hai. "
                f"Complaint ID {complaint_id} hai. "
                "Maintenance team isse already dekh rahi hai."
            )
        else:
            speak(
                f"{student['name']}, aapki hostel complaint register kar li gayi hai. "
                f"Complaint ID {complaint_id} hai. "
                "Isse 24 se 48 ghante ke andar resolve kar diya jayega."
            )

    else:
        speak(
            "Aapki complaint note kar li gayi hai. "
            "Maintenance team isse jaldi check karegi."
        )

else:
    speak(
        "Yeh issue automated system handle nahi karta. "
        "Please helpdesk staff se contact kijiye."
    )


# ---------- END ----------
speak("Thank you for calling MANIT helpdesk.")
speak("Have a nice day.")
