from django.contrib import admin
from exam_sessions.models import CourseExamSession, SubjectExamSession, FreeExamSession, ExamResults

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    exclude = ['questions']
    filter_horizontal = ('participants',)
    list_display=["session_name", 'course_exam', "exam_start"]

@admin.register(SubjectExamSession)
class SubjectExamSessionAdmin(admin.ModelAdmin):
    exclude = ['questions']
    filter_horizontal = ('participants',)

@admin.register(FreeExamSession)
class FreeExamSessionAdmin(admin.ModelAdmin):
    readonly_fields = ['session_ref_number']
    exclude =  ['subject_sessions', 'course_sessions']

@admin.register(ExamResults)
class ResultsExamAdmin(admin.ModelAdmin):
    list_display = ['student', 'get_session', 'created_at', 'is_finished', 'score', 'num_wrong']
