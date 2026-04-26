from django.urls import path
from . import views

urlpatterns = [
    path("", views.academy_access, name="academy_access"),
    path("student-info/", views.student_info, name="student_info"),

    path("skills/<str:student_id>/", views.skills_page, name="skills_page"),
    path("speaking/<str:student_id>/", views.speaking_page, name="speaking_page"),
    path("reading/<str:student_id>/", views.reading_page, name="reading_page"),

    path("listening/<str:student_id>/<str:level_name>/", views.listening_level_page, name="listening_level_page"),
    path("writing/<str:student_id>/<str:level_name>/", views.writing_level_page, name="writing_level_page"),

    path("result/<str:student_id>/", views.result_page, name="result_page"),

    path("teacher-login/", views.teacher_login, name="teacher_login"),
    path("teacher-logout/", views.teacher_logout, name="teacher_logout"),

    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("teacher-review/<str:student_id>/", views.teacher_review, name="teacher_review"),
    path("student-edit/<str:student_id>/", views.edit_student, name="edit_student"),
    path("student-delete/<str:student_id>/", views.delete_student, name="delete_student"),
]