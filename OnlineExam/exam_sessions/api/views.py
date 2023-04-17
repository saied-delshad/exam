from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import itertools
from datetime import datetime
from users.models import CustomUser
from exam_sessions.api.permissions import IsSubscribedInSession, ExamResultOwner, IsNetRise
from exam_sessions.api.serializers import (SubjectSessionSerializer, CourseSessionSerializer, SessionsSerializer,
                                           ExamResultSerializer, ExamResultWriteSerializer, FreeSessionSerializer)
from exam_sessions.models import SubjectExamSession, CourseExamSession, FreeExamSession, ExamResults
from questions.models import CourseModel


class SubjectSessionViewset(viewsets.ModelViewSet):
    queryset = SubjectExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = SubjectSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            # self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
            self.queryset = self.request.user.subject_exams.all()
        if taken_exams:
            for item in taken_exams:
               self.queryset =  self.queryset.exclude(session_ref_number = item.session_ref_number)
        return super(SubjectSessionViewset, self).get_queryset()

    


class CourseSessionViewset(viewsets.ModelViewSet):
    queryset = CourseExamSession.objects.all()
    lookup_field = "session_ref_number"
    serializer_class = CourseSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            # self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
            self.queryset = self.request.user.course_exams.all()
        if taken_exams:
            for item in taken_exams:
               self.queryset =  self.queryset.exclude(session_ref_number = item.session_ref_number)
        return super(CourseSessionViewset, self).get_queryset()


class ExamResultViewset(viewsets.ModelViewSet):
    queryset = ExamResults.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated, ExamResultOwner]
    lookup_field = "session_ref_number"

    def get_queryset(self):
        self.queryset = self.queryset.filter(student=self.request.user)
        return super(ExamResultViewset, self).get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            serializer_class = ExamResultSerializer
        else:
            serializer_class = ExamResultWriteSerializer
        return serializer_class
    def perform_create(self, serializer):
        serializer.save(student=self.request.user, 
                        session_ref_number=self.request.data.get('session_ref_number'))
        


class SessionsViewset(generics.ListAPIView):
    
    serializer_class = SessionsSerializer
    permission_classes = [IsNetRise]
    

    def get_queryset(self):
        course_name = self.kwargs.get('course')

        if course_name:
            try:
                course_exam = CourseModel.objects.get(course_name = course_name).course_exam
            except:
                course_exam = None
            return list(itertools.chain(CourseExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now(),
                                                                         course_exam = course_exam),
                                        FreeExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now())))
        else:
            return list(itertools.chain(CourseExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now()),
                                        FreeExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now())))
    
    

class SessionRegister(views.APIView):
    lookup_field = "session_ref_number"
    permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):

        applicant_nid = request.data.get('nid')
        session_ref_number = request.data.get('session_ref_code')
        applicant = CustomUser.get_or_create(username=applicant_nid, **request.data.get('applicant_data'))
        if session_ref_number.startswith('course_'):
            c_session = CourseExamSession.objects.get(session_ref_number=session_ref_number)
            if not applicant in c_session.participants.all():
                c_session.participants.add(applicant)
                return Response(request.data, status=status.HTTP_201_CREATED)
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        elif session_ref_number.startswith('free_'):
            f_exam = FreeExamSession.objects.get(session_ref_number=session_ref_number)
            course_name = request.data.get('course_name')
            try:
                course_exam = CourseModel.objects.get(course_name = course_name).course_exam
            except:
                course_exam = None
            if course_exam:
                try:
                    course_exam_session = f_exam.course_sessions.get(course_exam=course_exam)
                except:
                    course_exam_session = CourseExamSession.objects.create(course_exam = course_exam,
                                                                           session_name="fx-"+f_exam.session_ref_number,
                                                                           exam_start=f_exam.exam_start,
                                                                           show_score=f_exam.show_score)
                course_exam_session.participants.add(applicant)
                f_exam.increment_occupied()
                f_exam.course_sessions.add(course_exam_session)
            else:
                return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
            return Response(request.data, status=status.HTTP_201_CREATED)               


            







