
import json
from django.views.generic import DetailView
from exam_sessions.models import ExamResults, CourseExamSession, SessionParticipants as SP
from django.http import HttpResponseForbidden
from exam_sessions.send_scores import send_score
from django.shortcuts import redirect
from django.contrib import messages
from exam_sessions.html_to_pdf import render_to_pdf
from django.contrib.admin.views.decorators import staff_member_required
from core.utils import generate_random_string
import string



class ResultDetailView(DetailView):

    model = ExamResults
    context_object_name = 'result'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return HttpResponseForbidden
        return super(ResultDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snapshot = json.loads(context['result'].snapshot)
        q_list = snapshot['question_list']
        questions = json.loads(q_list)
        context["questions"] = questions
        context['session'] = context['result'].get_session()
        return context
    
    # def render_to_response(self, context, **response_kwargs):
    #     template = 'exam_sessions/examresults_detail.html'
    #     return render_to_pdf(
    #         template,
    #         context
    #     )



def sending_score(request, pk):

    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    else:
        result = ExamResults.objects.get(id=pk)

        if not result.fsession_ref_number:
            d_date = str(result.get_session().exam_start.date())
            t_date = str(result.get_session().exam_start.time())
            date = d_date + ' ' + t_date
            try:
                course_name = result.get_session().get_course()
                if course_name == 'IR(A)' or course_name=='IR(H)':
                    URL = 'https://bpms.cao.ir/NetForm/Service/irexamresult/request'
                else:
                    URL = 'https://bpms.cao.ir/NetForm/Service/examresult/request'

            except:
                URL = 'https://bpms.cao.ir/NetForm/Service/examresult/request'

            response = send_score(result.session_ref_number, 
                    result.student.username, 
                    str(result.score), 
                    date, 
                    passed = str(int(result.is_passed)), url=URL)
            try:
                response = response.json()
                result = response['result']
                if result:
                    messages.add_message(request, messages.INFO, response['message'])
                else:
                    messages.add_message(request, messages.WARNING, response['message'])
            except:
                messages.add_message(request, messages.WARNING, 'Something went wrong status code:' + str(response.status_code))
            return redirect('/admin/exam_sessions/examresults/')
        

def send_abscents(request, pk):
    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden()
    es_obj = CourseExamSession.objects.get(id=pk)
    session_ref = es_obj.session_ref_number
    results = ExamResults.objects.filter(session_ref_number = session_ref)
    abscents = es_obj.participants.exclude(id__in = results.values_list('student', flat=True))
    
    if abscents.count() > 0:
        for student in abscents:
            ExamResults.objects.create(student=student, session_ref_number=session_ref, score=0, is_finished=True,
                                       is_abscent = True)

    return redirect('/admin/exam_sessions/courseexamsession/')



@staff_member_required
def list_participants(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    #students = exam_session.participants.all()
    if not exam_session.is_active and not exam_session.started:
        students = SP.objects.filter(session = exam_session)
        for student in students:
            password = generate_random_string(chars=string.digits, length=6)
            student.applicant.set_password(password)
            student.applicant.save()
            student.passw = password
    else:
        students = None
    context = {'students': students, 'session_name': exam_session.session_name, 
            'session_time': exam_session.exam_start}
    template = 'exam_sessions/participants.html'
    return render_to_pdf(
            template,
            context
        )


@staff_member_required
def exam_papers(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    students = exam_session.participants.all()
    context = {'students': students, 'session_name': exam_session.session_name}
    template = 'exam_sessions/participants.html'
    return render_to_pdf(
            template,
            context
        )

@staff_member_required
def start_session(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    if exam_session.started:
        exam_session.started = False
        exam_session.save()
    else:
        exam_session.started = True
        exam_session.save()
    return redirect('/admin/exam_sessions/courseexamsession/')

@staff_member_required
def register_status(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    if exam_session.is_active:
        exam_session.is_active = False
        exam_session.save()
    else:
        exam_session.is_active = True
        exam_session.save()
    return redirect('/admin/exam_sessions/courseexamsession/')
