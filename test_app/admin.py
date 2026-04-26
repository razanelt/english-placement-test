from django.contrib import admin
from .models import StudentResult


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "student_id",
        "speaking_score",
        "listening_score",
        "reading_score",
        "writing_score",
        "total_score",
        "overall_level",
    )
    search_fields = ("full_name", "student_id")