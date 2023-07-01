
import os
from django.views.generic import DetailView
from django.conf import settings
from exam_sessions.models import ExamResults, CourseExamSession
from django.http import HttpResponseForbidden
from exam_sessions.send_scores import send_score
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from exam_sessions.html_to_pdf import render_to_pdf



class ResultDetailView(DetailView):

    model = ExamResults
    context_object_name = 'result'



def sending_score(request, pk):

    if not request.user.is_staff or not request.user.is_superuser:
        return HttpResponseForbidden
    else:
        result = ExamResults.objects.get(id=pk)

        if not result.fsession_ref_number:
            d_date = str(result.get_session().exam_start.date())
            t_date = str(result.get_session().exam_start.time())
            date = d_date + ' ' + t_date

            response = send_score(result.session_ref_number, 
                    result.student.username, 
                    str(result.score), 
                    date, 
                    passed = str(int(result.is_passed)))
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

