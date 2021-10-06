from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from questions.api.serializers import QuestionSerializer
from questions.models import QuestionModel
from exam_sessions.models import SubjectExamSession, CourseExamSession
from questions.api.permissions import IsSubscribedInSession



class QuestionViewset(viewsets.ModelViewSet):
    queryset = QuestionModel.objects.all()
    lookup_field = "question_ref_code"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsSubscribedInSession]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


    def get_queryset(self):
        
        ref = self.kwargs['session_ref']
        questios_queryset = subject_exam = None
        try:
            subject_exam = SubjectExamSession.objects.get(session_ref_number=ref)
        except:
            pass
        if subject_exam:
            questios_queryset = subject_exam.questions.all()
        return questios_queryset
