from django.contrib import admin
from exam_sessions.models import CourseExamSession, SubjectExamSession, ExamResults
from django.db import models

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']
    filter_horizontal = ('participants',)

@admin.register(SubjectExamSession)
class SubjectExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']
    filter_horizontal = ('participants',)

@admin.register(ExamResults)
class ResultsExamAdmin(admin.ModelAdmin):
    list_display = ['student', 'created_at', 'is_finished', 'score']