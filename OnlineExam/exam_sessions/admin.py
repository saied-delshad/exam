from django.contrib import admin
from exam_sessions.models import CourseExamSession, SubjectExamSession, ExamResults

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']

@admin.register(SubjectExamSession)
class SubjectExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']

@admin.register(ExamResults)
class ResultsExamAdmin(admin.ModelAdmin):
    list_display = ['student', 'created_at', 'is_finished', 'score']