from django.db import models


class StudentResult(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    student_id = models.CharField(max_length=100, unique=True)

    listening_answers = models.JSONField(default=dict, blank=True)
    writing_answers = models.JSONField(default=dict, blank=True)

    listening_reached_level = models.CharField(max_length=50, default="Not started")
    writing_reached_level = models.CharField(max_length=50, default="Not started")

    listening_done = models.BooleanField(default=False)
    writing_done = models.BooleanField(default=False)

    speaking_score = models.PositiveIntegerField(default=0)
    listening_score = models.PositiveIntegerField(default=0)
    reading_score = models.PositiveIntegerField(default=0)
    writing_score = models.PositiveIntegerField(default=0)

    speaking_level = models.CharField(max_length=50, default="Seeds")
    listening_level = models.CharField(max_length=50, default="Seeds")
    reading_level = models.CharField(max_length=50, default="Seeds")
    writing_level = models.CharField(max_length=50, default="Seeds")

    @property
    def total_score(self):
        return (
            self.speaking_score
            + self.listening_score
            + self.reading_score
            + self.writing_score
        )

    @property
    def overall_level(self):
        total = self.total_score
        if total <= 10:
            return "Seeds"
        elif total <= 20:
            return "Sparks"
        elif total <= 30:
            return "Rays"
        return "Crystals"

    def __str__(self):
        return f"{self.full_name} - {self.student_id}"