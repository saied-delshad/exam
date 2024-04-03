from typing import Any, List, Tuple
from django.contrib import admin
from django.http.request import HttpRequest
from users.models import CustomUser
from exam_sessions.models import CourseExamSession, SubjectExamSession, FreeExamSession, ExamResults, SessionParticipants
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from datetime import datetime



class CurrentExamsFilter(admin.SimpleListFilter):
    title = ("Show current exams")
    parameter_name = "currents"

    def lookups(self, request, model_admin):
        
        return [
        ("Currents", "Current Exams"),
        ("Pasts", "Past Exams"),
        ]
    
    def queryset(self, request, queryset):

        if self.value() == "Currents":
            return queryset.filter(
                exam_start__gte=datetime.now()
            )
        if self.value() == "Pasts":
            return queryset.filter(
                exam_start__lt=datetime.now(),
                )

class ParticipantsForm(admin.TabularInline):
    model = SessionParticipants
    readonly_fields = ['registration_date_time']
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False
    

@admin.register(CourseExamSession)
class CourseExamSessionAdmin(admin.ModelAdmin):
    exclude = ['questions']
    # filter_horizontal = ('participants',)
    list_display=["session_name", 'course_exam', "exam_start", "show_participantes", 'seats_occupied', 'start_session',
                  'register_status', 'send_abscents']
    list_filter = ['course_exam', CurrentExamsFilter]
    search_fields = ['session_name', 'exam_start', 'participants__username']
    inlines = (ParticipantsForm,)



    def changelist_view(self, request, extra_context=None):
        if not (request.user.is_superuser or request.user.username=='exam_admin'):
            self.list_display = ['session_name', 'course_exam', "exam_start", "show_participantes"]
        return super(CourseExamSessionAdmin, self).changelist_view(request, extra_context)


    def show_participantes(self, obj):
        if obj.started:
            return format_html('<a  href="/exam-sessions/participants/{0}" target="_blank">list participants</a>&nbsp;', obj.id )
        else:
            return None
    show_participantes.short_description = 'List Participants'
    show_participantes.allow_tags = True


    def seats_occupied(sel, obj):
        return obj.session_occupied_seats()
    
    def start_session(self, obj):
        if obj.started:
            return format_html('<a  href="/exam-sessions/session-start/{0}" style="color:red;"><img src="{1}" alt="stop" style="height:30px;"/></a>&nbsp;', obj.id, '/media/imgs/stop.jpg')
        else:
            return format_html('<a  href="/exam-sessions/session-start/{0}" style="color:green;"><img src="{1}" alt="play" style="height:30px;"/></a>&nbsp;', obj.id, '/media/imgs/play.jpg' )
    start_session.short_description = 'Start/Stop Session'
    start_session.allow_tags = True

    def register_status(self, obj):
        if obj.is_active:
            return format_html('<a  href="/exam-sessions/register-status/{0}" style="color:red;"><img src="{1}" alt="close" style="height:50px;"/></a>&nbsp;', obj.id, '/media/imgs/open.jpg' )
        else:
            return format_html('<a  href="/exam-sessions/register-status/{0}" style="color:green;"><img src="{1}" alt="open" style="height:50px;"/></a>&nbsp;', obj.id, '/media/imgs/closed.jpg' )
    register_status.short_description = 'Register Open/Close'
    register_status.allow_tags = True

    def send_abscents(self, obj):
        return format_html('<a  href="/exam-sessions/abscents-send/{0}">Send Abscents</a>&nbsp;', obj.id )
    register_status.short_description = 'Send Abscents'
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
class ResultsExamAdmin(ImportExportModelAdmin):
    list_display = ['student', 'created_at', 'is_finished', 'score', 'is_abscent', 'show_transcript', 'send_score', 'course']
    search_fields = ['student__username', 'student__last_name', 'session_ref_number']


    def show_transcript(self, obj):
        return format_html('<a  href="/exam-sessions/transcript/{0}" target="_blank">show transcript</a>&nbsp;', obj.id )
    show_transcript.short_description = 'Show Transcript'
    show_transcript.allow_tags = True


    def send_score(self, obj):
        return format_html('<a  href="/exam-sessions/score-send/{0}" >send score</a>&nbsp;', obj.id )
    send_score.short_description = 'Send Score to PEL'
    send_score.allow_tags = True


    def course(self, obj):
        return obj.get_session().session_name
    course.short_description = 'Session name'