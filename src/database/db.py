from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode(),
        bcrypt.gensalt()
    ).decode()


def check_pass(pwd, hashed):
    return bcrypt.checkpw(
        pwd.encode(),
        hashed.encode()
    )


def check_teacher_exists(username):
    response = (
        supabase
        .table("teachers")
        .select("username")
        .eq("username", username)
        .execute()
    )

    return len(response.data) > 0


def create_teacher(username, password, name):

    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }

    response = (
        supabase
        .table("teachers")
        .insert(data)
        .execute()
    )

    return response.data


def teacher_login(username, password):

    response = (
        supabase
        .table("teachers")
        .select("*")
        .eq("username", username)
        .execute()
    )

    if response.data:
        teacher = response.data[0]

        if check_pass(password, teacher["password"]):
            return teacher

    return None


def get_all_students():

    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    return response.data


def create_subject(subject_code, name, section, teacher_id):

    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id
    }

    response = (
        supabase
        .table("subjects")
        .insert(data)
        .execute()
    )

    return response.data


def get_teacher_subjects(teacher_id):

    response = (
        supabase
        .table("subjects")
        .select(
            "*,subject_students(count),attandance_logs(timestamp)"
        )
        .eq("teacher_id", teacher_id)
        .execute()
    )

    subjects = response.data

    for sub in subjects:

        # Count students
        student_data = sub.get("subject_students", [])

        if student_data:
            sub["total_students"] = student_data[0].get("count", 0)
        else:
            sub["total_students"] = 0

        # Count unique attendance sessions
        attendance = sub.get("attandance_logs", [])

        unique_sessions = len(
            set(
                log.get("timestamp")
                for log in attendance
                if log.get("timestamp")
            )
        )

        sub["total_classes"] = unique_sessions

        # Remove nested data
        sub.pop("subject_students", None)
        sub.pop("attandance_logs", None)

    return subjects




