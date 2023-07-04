from django.contrib import admin
from exam_sessions.models import CourseExamSession, SubjectExamSession, FreeExamSession, ExamResults
from django.utils.html import format_html
from exam_sessions.send_scores import send_score

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    # pass
    exclude = ['questions']
    filter_horizontal = ('participants',)
    list_display=["session_name", 'course_exam', "exam_start", "show_participantes", 'seats_occupied', 'start_session',
                  'register_status']


    def show_participantes(self, obj):
        return format_html('<a  href="/exam-sessions/participants/{0}" target="_blank">list participants</a>&nbsp;', obj.id )
    show_participantes.short_description = 'List Participants'
    show_participantes.allow_tags = True


    def seats_occupied(sel, obj):
        return obj.session_occupied_seats()
    
    def start_session(self, obj):
        if obj.started:
            return format_html('<a  href="/exam-sessions/session-start/{0}" style="color:red;">STOP</a>&nbsp;', obj.id )
        else:
            return format_html('<a  href="/exam-sessions/session-start/{0}" style="color:green;">START</a>&nbsp;', obj.id )
    start_session.short_description = 'Start/Stop Session'
    start_session.allow_tags = True

    def register_status(self, obj):
        if obj.is_active:
            return format_html('<a  href="/exam-sessions/register-status/{0}" style="color:red;">Close Registeration</a>&nbsp;', obj.id )
        else:
            return format_html('<a  href="/exam-sessions/register-status/{0}" style="color:green;">Open Registeration</a>&nbsp;', obj.id )
    register_status.short_description = 'Register Open/Close'
    register_status.allow_tags = True

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