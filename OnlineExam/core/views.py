from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from exam_sessions.models import ExamResults

class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        active_exam = ExamResults.objects.filter(student = request.user, is_finished = False).first()
        if active_exam and request.get_full_path() == "/":
            if active_exam.session_ref_number:
                return redirect('/'+active_exam.session_ref_number)
        else:
            return super(IndexTemplateView, self).get(request, *args, **kwargs)


    def get_template_names(self):
        if not settings.DEBUG:
            template_name = 'index-dev.html'
        else:
            template_name = 'index.html'
        return template_name