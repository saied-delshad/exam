from django.contrib import admin
from exam_sessions.models import CourseExamSession, SubjectExamSession, FreeExamSession, ExamResults
from django.utils.html import format_html
from exam_sessions.send_scores import send_score

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']
    filter_horizontal = ('participants',)
    list_display=["session_name", 'course_exam', "exam_start", "show_participantes", 'seats_occupied']


    def show_participantes(self, obj):
        return format_html('<a  href="/exam-sessions/participants/{0}" target="_blank">list participants</a>&nbsp;', obj.id )
    show_participantes.short_description = 'List Participants'
    show_participantes.allow_tags = True


    def seats_occupied(sel, obj):
        return obj.session_occupied_seats()

@admin.register(SubjectExamSession)
class SubjectExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']
    filter_horizontal = ('participants',)

@admin.register(FreeExamSession)
class FreeExamSessionAdmin(admin.ModelAdmin):
    readonly_fields = ['session_ref_number']
    exclude =  ['subject_sessions', 'course_sessions']

@admin.register(ExamResults)
class ResultsExamAdmin(admin.ModelAdmin):
    list_display = ['student', 'created_at', 'is_finished', 'score', 'show_transcript', 'send_score']

    def show_transcript(self, obj):
        return format_html('<a  href="/exam-sessions/transcript/{0}" target="_blank">show transcript</a>&nbsp;', obj.id )
    show_transcript.short_description = 'Show Transcript'
    show_transcript.allow_tags = True


    def send_score(self, obj):
        return format_html('<a  href="/exam-sessions/score-send/{0}" >send score</a>&nbsp;', obj.id )
    send_score.short_description = 'Send Score to PEL'
    send_score.allow_tags = True