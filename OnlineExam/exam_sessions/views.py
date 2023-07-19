
import json
from django.views.generic import DetailView
from exam_sessions.models import ExamResults, CourseExamSession
from django.http import HttpResponseForbidden
from exam_sessions.send_scores import send_score
from django.shortcuts import redirect
from django.contrib import messages
from exam_sessions.html_to_pdf import render_to_pdf



class ResultDetailView(DetailView):

    model = ExamResults
    context_object_name = 'result'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
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
        return HttpResponseForbidden
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
            print(response)
            if response['result']:
                messages.add_message(request, messages.INFO, response['message'])
            else:
                messages.add_message(request, messages.WARNING, response['message'])
            return redirect('/admin/exam_sessions/examresults/')







def list_participants(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    students = exam_session.participants.all()
    context = {'students': students, 'session_name': exam_session.session_name}
    template = 'exam_sessions/participants.html'
    return render_to_pdf(
            template,
            context
        )



def start_session(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    if exam_session.started:
        exam_session.started = False
        exam_session.save()
    else:
        exam_session.started = True
        exam_session.save()
    return redirect('/admin/exam_sessions/courseexamsession/')

def register_status(request, pk):
    exam_session = CourseExamSession.objects.get(id=pk)
    if exam_session.is_active:
        exam_session.is_active = False
        exam_session.save()
    else:
        exam_session.is_active = True
        exam_session.save()
    return redirect('/admin/exam_sessions/courseexamsession/')
