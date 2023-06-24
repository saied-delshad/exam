from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from questions.api.serializers import QuestionSerializer
from questions.models import QuestionModel
from exam_sessions.models import SubjectExamSession, CourseExamSession, ExamResults
from questions.api.permissions import IsSubscribedInSession
from rest_framework.exceptions import PermissionDenied



class QuestionViewset(viewsets.ModelViewSet):
    queryset = QuestionModel.objects.all()
    lookup_field = "question_ref_code"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)

    def get_queryset(self):

        ref = self.kwargs['session_ref']
        questios_queryset = subject_exam = None
        try:
            try:
                
                result = ExamResults.objects.get(student=self.request.user, session_ref_number=ref)
                if result.is_finished:
                    self.queryset = self.queryset.none()
                    return super(QuestionViewset, self).get_queryset()
            except:
                pass
            if ref.startswith('sub'):
                subject_exam = SubjectExamSession.objects.get(session_ref_number=ref)
                self.queryset = subject_exam.questions.all()
            elif ref.startswith('course'):
                course_exam = CourseExamSession.objects.get(session_ref_number=ref)
                self.queryset = course_exam.questions.all()
            else:
                self.queryset = self.queryset.none()
        except:
            if not self.request.user.is_superuser:
                self.queryset = self.queryset.none()
                
           
        return super(QuestionViewset, self).get_queryset()
