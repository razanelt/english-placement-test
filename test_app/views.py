from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import StudentResult


ACADEMY_ACCESS_CODE = "UPPERSKILLS2026"

LISTENING_DATA = {
    "Seeds": {
        "title": "Seeds",
        "instruction": "Listen and write the instruction.",
        "audio_files": [
            "test_app/audio/seeds1.mp4",
            "test_app/audio/seeds2.mp4",
        ],
        "prompt": [
            "Listen to the 2 audio files and answer.",
        ],
        "questions": [
            "Write the first instruction:",
            "Write the second instruction:",
        ],
    },
    "Sparks": {
        "title": "Sparks",
        "instruction": "Listen and write the sentence or command.",
        "audio_files": [
            "test_app/audio/sparks1.mp4",
            "test_app/audio/sparks2.mp4",
            "test_app/audio/sparks3.mp4",
        ],
        "prompt": [
            "Listen to the 3 audio files and answer.",
        ],
        "questions": [
            "Write the first command:",
            "Write the second command:",
            "Write the third command:",
        ],
    },
    "Rays": {
        "title": "Rays",
        "instruction": "Listen and answer.",
        "audio_files": [
            "test_app/audio/rays.mp4",
        ],
        "prompt": [
            "Listen carefully and answer the questions.",
        ],
        "questions": [
            "What color is the bike?",
            "How many bikes does he have?",
        ],
    },
    "Crystals": {
        "title": "Crystals",
        "instruction": "Listen and answer.",
        "audio_files": [
            "test_app/audio/crystals.mp4",
        ],
        "prompt": [
            "Listen carefully and answer the questions.",
        ],
        "questions": [
            "Where did I go?",
            "Who did I go with?",
            "What did we do?",
        ],
    },
}

WRITING_DATA = {
    "Seeds": {
        "title": "Seeds",
        "instruction": "Complete the beginner writing tasks.",
        "image": None,
        "prompt": [
            "Write your name.",
            "Copy: cat, dog, book",
        ],
        "questions": [
            "Write your name:",
            "Copy the words:",
        ],
    },
    "Sparks": {
        "title": "Sparks",
        "instruction": "Complete the sentence tasks.",
        "image": None,
        "prompt": [
            "Complete the two sentences.",
        ],
        "questions": [
            "Sentence 1: I am ___ years old.",
            "Sentence 2: I like ___.",
        ],
    },
    "Rays": {
        "title": "Rays",
        "instruction": "Write 2 sentences to describe the picture.",
        "image": "test_app/images/writing_rays.png",
        "prompt": [
            "Look at the picture and write 2 different sentences.",
        ],
        "questions": [
            "Sentence 1:",
            "Sentence 2:",
        ],
    },
    "Crystals": {
        "title": "Crystals",
        "instruction": "Write 3 sentences to describe the picture.",
        "image": "test_app/images/writing_crystals.png",
        "prompt": [
            "Look at the picture and write 3 different sentences.",
        ],
        "questions": [
            "Sentence 1:",
            "Sentence 2:",
            "Sentence 3:",
        ],
    },
}

LEVELS = ["Seeds", "Sparks", "Rays", "Crystals"]


def academy_access(request):
    error_message = ""

    if request.session.get("academy_access_granted"):
        return redirect("student_info")

    if request.method == "POST":
        entered_code = request.POST.get("academy_code", "").strip()

        if entered_code == ACADEMY_ACCESS_CODE:
            request.session["academy_access_granted"] = True
            return redirect("student_info")
        else:
            error_message = "Invalid academy code. Please try again."

    return render(
        request,
        "test_app/academy_access.html",
        {"error_message": error_message},
    )


def teacher_login(request):
    error_message = ""

    if request.user.is_authenticated:
        return redirect("admin_dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        else:
            error_message = "Invalid teacher username or password."

    return render(
        request,
        "test_app/teacher_login.html",
        {"error_message": error_message},
    )


@login_required(login_url="teacher_login")
def teacher_logout(request):
    logout(request)
    return redirect("teacher_login")


def student_info(request):
    if not request.session.get("academy_access_granted"):
        return redirect("academy_access")

    error_message = ""

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        age = request.POST.get("age", "").strip()
        student_id = request.POST.get("student_id", "").strip()

        if first_name and last_name and age and student_id:
            full_name = f"{first_name} {last_name}"

            existing_student = StudentResult.objects.filter(student_id=student_id).first()

            if existing_student:
                existing_student.full_name = full_name
                existing_student.age = int(age)
                existing_student.save()
                return redirect("skills_page", student_id=existing_student.student_id)

            student = StudentResult.objects.create(
                full_name=full_name,
                age=int(age),
                student_id=student_id,
            )

            return redirect("skills_page", student_id=student.student_id)
        else:
            error_message = "Please fill in all required fields."

    return render(
        request,
        "test_app/student_info.html",
        {
            "error_message": error_message,
        },
    )


def skills_page(request, student_id):
    if not request.session.get("academy_access_granted"):
        return redirect("academy_access")

    student = get_object_or_404(StudentResult, student_id=student_id)
    success_message = request.GET.get("success", "")

    return render(
        request,
        "test_app/skills.html",
        {
            "student": student,
            "success_message": success_message,
        },
    )


def speaking_page(request, student_id):
    if not request.session.get("academy_access_granted"):
        return redirect("academy_access")

    student = get_object_or_404(StudentResult, student_id=student_id)
    return render(request, "test_app/speaking.html", {"student": student})


def reading_page(request, student_id):
    if not request.session.get("academy_access_granted"):
        return redirect("academy_access")

    student = get_object_or_404(StudentResult, student_id=student_id)
    return render(request, "test_app/reading.html", {"student": student})


def _build_answer_dict(post_data, questions_count):
    answers = {}
    for i in range(1, questions_count + 1):
        answers[f"q{i}"] = post_data.get(f"q{i}", "").strip()
    return answers


def _progressive_skill_handler(request, student_id, level_name, skill_name, skill_data):
    if not request.session.get("academy_access_granted"):
        return redirect("academy_access")

    student = get_object_or_404(StudentResult, student_id=student_id)

    if level_name not in skill_data:
        return redirect("skills_page", student_id=student.student_id)

    if skill_name == "Listening" and student.listening_done:
        url = reverse("skills_page", kwargs={"student_id": student.student_id})
        return redirect(f"{url}?success=Listening already completed")

    if skill_name == "Writing" and student.writing_done:
        url = reverse("skills_page", kwargs={"student_id": student.student_id})
        return redirect(f"{url}?success=Writing already completed")

    current_index = LEVELS.index(level_name)
    total_steps = len(LEVELS)
    current_step = current_index + 1
    level_data = skill_data[level_name]

    if request.method == "POST":
        remaining_seconds = int(request.POST.get("remaining_seconds", 0) or 0)
        time_up = request.POST.get("time_up", "0") == "1"
        answers = _build_answer_dict(request.POST, len(level_data["questions"]))

        if skill_name == "Listening":
            all_answers = student.listening_answers or {}
            all_answers[level_name] = answers
            student.listening_answers = all_answers
            student.listening_reached_level = level_name
        else:
            all_answers = student.writing_answers or {}
            all_answers[level_name] = answers
            student.writing_answers = all_answers
            student.writing_reached_level = level_name

        if time_up or remaining_seconds <= 0 or current_index == total_steps - 1:
            if skill_name == "Listening":
                student.listening_done = True
                student.save()
                url = reverse("skills_page", kwargs={"student_id": student.student_id})
                return redirect(f"{url}?success=Listening test completed")
            else:
                student.writing_done = True
                student.save()
                url = reverse("skills_page", kwargs={"student_id": student.student_id})
                return redirect(f"{url}?success=Writing test completed")

        student.save()

        next_level = LEVELS[current_index + 1]

        if skill_name == "Listening":
            return redirect(
                "listening_level_page",
                student_id=student.student_id,
                level_name=next_level,
            )
        else:
            return redirect(
                "writing_level_page",
                student_id=student.student_id,
                level_name=next_level,
            )

    remaining_seconds = 240

    return render(
        request,
        "test_app/progressive_skill.html",
        {
            "student": student,
            "skill_name": skill_name,
            "level_name": level_name,
            "level_data": level_data,
            "current_step": current_step,
            "total_steps": total_steps,
            "remaining_seconds": remaining_seconds,
        },
    )


def listening_level_page(request, student_id, level_name):
    return _progressive_skill_handler(
        request=request,
        student_id=student_id,
        level_name=level_name,
        skill_name="Listening",
        skill_data=LISTENING_DATA,
    )


def writing_level_page(request, student_id, level_name):
    return _progressive_skill_handler(
        request=request,
        student_id=student_id,
        level_name=level_name,
        skill_name="Writing",
        skill_data=WRITING_DATA,
    )


def result_page(request, student_id):
    student = get_object_or_404(StudentResult, student_id=student_id)
    return render(request, "test_app/result.html", {"student": student})


@login_required(login_url="teacher_login")
def admin_dashboard(request):
    search_query = request.GET.get("q", "").strip()

    students = StudentResult.objects.all().order_by("-id")

    if search_query:
        students = StudentResult.objects.filter(
            full_name__icontains=search_query
        ) | StudentResult.objects.filter(
            student_id__icontains=search_query
        )
        students = students.order_by("-id")

    return render(
        request,
        "test_app/admin_dashboard.html",
        {
            "students": students,
            "total_students": StudentResult.objects.count(),
            "search_query": search_query,
        },
    )


@login_required(login_url="teacher_login")
def teacher_review(request, student_id):
    student = get_object_or_404(StudentResult, student_id=student_id)

    if request.method == "POST":
        student.speaking_score = int(request.POST.get("speaking_score", 0) or 0)
        student.listening_score = int(request.POST.get("listening_score", 0) or 0)
        student.reading_score = int(request.POST.get("reading_score", 0) or 0)
        student.writing_score = int(request.POST.get("writing_score", 0) or 0)

        student.speaking_level = request.POST.get("speaking_level", "Seeds")
        student.listening_level = request.POST.get("listening_level", "Seeds")
        student.reading_level = request.POST.get("reading_level", "Seeds")
        student.writing_level = request.POST.get("writing_level", "Seeds")

        student.save()
        return redirect("teacher_review", student_id=student.student_id)

    listening_answers = student.listening_answers or {}
    writing_answers = student.writing_answers or {}

    listening_sections = []
    for level_name, answers in listening_answers.items():
        questions_list = []
        for q_key, q_value in answers.items():
            questions_list.append(
                {
                    "question_key": q_key,
                    "answer": q_value if q_value else "No answer",
                }
            )
        listening_sections.append(
            {
                "level": level_name,
                "questions": questions_list,
            }
        )

    writing_sections = []
    for level_name, answers in writing_answers.items():
        questions_list = []
        for q_key, q_value in answers.items():
            questions_list.append(
                {
                    "question_key": q_key,
                    "answer": q_value if q_value else "No answer",
                }
            )
        writing_sections.append(
            {
                "level": level_name,
                "questions": questions_list,
            }
        )

    return render(
        request,
        "test_app/teacher_review.html",
        {
            "student": student,
            "listening_sections": listening_sections,
            "writing_sections": writing_sections,
        },
    )


@login_required(login_url="teacher_login")
def edit_student(request, student_id):
    student = get_object_or_404(StudentResult, student_id=student_id)

    if request.method == "POST":
        new_full_name = request.POST.get("full_name", student.full_name).strip()
        new_age = request.POST.get("age", student.age)
        new_student_id = request.POST.get("student_id", student.student_id).strip()

        student.full_name = new_full_name
        student.age = int(new_age)
        student.student_id = new_student_id
        student.save()

        return redirect("admin_dashboard")

    return render(request, "test_app/edit_student.html", {"student": student})


@login_required(login_url="teacher_login")
def delete_student(request, student_id):
    student = get_object_or_404(StudentResult, student_id=student_id)

    if request.method == "POST":
        student.delete()
        return redirect("admin_dashboard")

    return render(request, "test_app/delete_student.html", {"student": student})