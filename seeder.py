import requests
import random
from datetime import timedelta, time, date

API_BASE = "http://127.0.0.1:8000"

NUM_TEACHERS = 10
NUM_SUBJECTS = 8
NUM_LESSONS = 200

FIRST_LESSON_DATE = date.today()

TEACHER_NAMES = [
    "John Smith",
    "Michael Johnson",
    "Robert Williams",
    "Emily Brown",
    "Oliver Jones",
    "Sophia Miller",
    "James Davis",
    "Emma Wilson",
    "Benjamin Taylor",
    "Charlotte Anderson",
]

SUBJECT_NAMES = [
    "Mathematics",
    "Physics",
    "Computer Science",
    "History",
    "Biology",
    "Chemistry",
    "Literature",
    "English Language",
]


CLASSROOMS = ["101", "102", "201", "202", "301", "302", "303"]
GROUPS = ["A", "B", "C", "D"]
LESSON_TYPES = ["lecture", "seminar", "lab"]


def create_teacher(session, payload):
    r = session.post(f"{API_BASE}/teachers", json=payload)
    r.raise_for_status()
    return r.json()


def create_subject(session, payload):
    r = session.post(f"{API_BASE}/subjects", json=payload)
    r.raise_for_status()
    return r.json()


def create_lesson(session, payload):
    r = session.post(f"{API_BASE}/lessons", json=payload)
    r.raise_for_status()
    return r.json()


def main():
    session = requests.Session()

    print(f"Creating {NUM_TEACHERS} teachers...")
    teacher_ids = []
    for i in range(NUM_TEACHERS):
        name = TEACHER_NAMES[i % len(TEACHER_NAMES)] + ("" if i < len(TEACHER_NAMES) else f" #{i}")
        payload = {
            "full_name": name,
            "department": random.choice(["Math", "Pyscics", "informatics", "humanitry"]),
            "position": random.choice(["lecturer", "Doctor", "professor"]),
            "degree": random.choice(["PhD", "MSc", "Doctor philosofy", None])
        }
        try:
            obj = create_teacher(session, payload)
            teacher_ids.append(obj["id"]) if isinstance(obj, dict) and "id" in obj else teacher_ids.append(obj["id"])
        except Exception as e:
            print("Failed creating teacher:", e)
    print(f"Created {len(teacher_ids)} teachers")

    print(f"Creating {NUM_SUBJECTS} subjects...")
    subject_ids = []
    for i in range(NUM_SUBJECTS):
        name = SUBJECT_NAMES[i % len(SUBJECT_NAMES)] + ("" if i < len(SUBJECT_NAMES) else f" #{i}")
        payload = {
            "name": name,
            "hours": random.choice([30, 45, 60, 90]),
            "exam_type": random.choice(["exam", "credit"]),
            "required": random.choice(["yes", "no"]),
        }
        try:
            obj = create_subject(session, payload)
            subject_ids.append(obj["id"])
        except Exception as e:
            print("Failed creating subject:", e)
    print(f"Created {len(subject_ids)} subjects")

    if not teacher_ids or not subject_ids:
        print("Need at least one teacher and one subject to create lessons. Exiting.")
        return

    print(f"Creating {NUM_LESSONS} lessons...")
    created = 0
    for i in range(NUM_LESSONS):
        lesson_date = FIRST_LESSON_DATE + timedelta(days=random.randint(0, 60))
        lesson_time = time(hour=random.choice([8, 10, 12, 14, 16]))
        payload = {
            "date": lesson_date.isoformat(),
            "time": lesson_time.strftime("%H:%M:%S"),
            "classroom": random.choice(CLASSROOMS),
            "group": random.choice(GROUPS),
            "lesson_type": random.choice(LESSON_TYPES),
            "teacher_id": random.choice(teacher_ids),
            "subject_id": random.choice(subject_ids),
        }
        try:
            create_lesson(session, payload)
            created += 1
            if created % 20 == 0:
                print(f"  {created} lessons created")
        except Exception as e:
            print(f"Failed creating lesson #{i}:", e)
    print(f"Finished creating {created} lessons")


if __name__ == '__main__':
    main()
