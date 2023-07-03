from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import itertools
from datetime import datetime
from users.models import CustomUser
from exam_sessions.api.permissions import IsSubscribedInSession, ExamResultOwner, IsNetRise
from exam_sessions.api.serializers import (SubjectSessionSerializer, CourseSessionSerializer, SessionsSerializer,
                                           ExamResultSerializer, ExamResultWriteSerializer, FreeSessionSerializer)
from exam_sessions.models import SubjectExamSession, CourseExamSession, FreeExamSession, ExamResults
from questions.models import CourseModel
from core.sms_send import send_sms
from core.image_upload import photo


class SubjectSessionViewset(viewsets.ModelViewSet):
    queryset = SubjectExamSession.objects.filter(started=True)
    lookup_field = "session_ref_number"
    serializer_class = SubjectSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            # self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
            self.queryset = self.request.user.subject_exams.filter(started=True)
        if taken_exams:
            for item in taken_exams:
               self.queryset =  self.queryset.exclude(session_ref_number = item.session_ref_number)
        return super(SubjectSessionViewset, self).get_queryset()

    


class CourseSessionViewset(viewsets.ModelViewSet):
    queryset = CourseExamSession.objects.filter(started=True)
    lookup_field = "session_ref_number"
    serializer_class = CourseSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        taken_exams = ExamResults.objects.filter(student = self.request.user)
        if self.request.user.is_authenticated:
            # self.queryset = self.queryset.filter(participants__in=self.request.user.groups.all())
            self.queryset = self.request.user.course_exams.filter(started=True)
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

            course_exam_sessions = CourseExamSession.objects.filter(~Q(session_name__startswith='fx-free'),
                                                    is_active=True, exam_start__gt= datetime.now(),
                                                    course_exam = course_exam)
            for session in course_exam_sessions:
                if session.remaining_seats()<=0:
                    course_exam_sessions = course_exam_sessions.exclude(id = session.id)
            return list(itertools.chain(course_exam_sessions,
                                        FreeExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now())))
        else:
            course_exam_sessions = CourseExamSession.objects.filter(~Q(session_name__startswith='fx-free'),
                                        is_active=True, exam_start__gt= datetime.now())
            for session in course_exam_sessions:
                if session.remaining_seats()<=0:
                    course_exam_sessions = course_exam_sessions.exclude(id = session.id)
            print(course_exam_sessions)
            return list(itertools.chain(course_exam_sessions,
                                        FreeExamSession.objects.filter(is_active=True, exam_start__gt= datetime.now())))
    
    

class SessionRegister(views.APIView):
    lookup_field = "session_ref_number"
    permission_classes = [IsAuthenticated]
    
    @csrf_exempt
    def post(self, request, *args, **kwargs):

        applicant_nid = request.data.get('nid')
        session_ref_number = request.data.get('session_ref_code')
        app_data = request.data.get('applicant_data')
        photo_data = app_data.pop('photo', None)

        applicant = CustomUser.get_or_create(username=applicant_nid, **app_data)
        if photo_data and not applicant.photo:
            photo_file = photo(photo_data, applicant_nid)
            applicant.photo.save(photo_file[0], photo_file[1], save=True)
        if session_ref_number.startswith('course_'):
            c_session = CourseExamSession.objects.get(session_ref_number=session_ref_number)
            if not applicant in c_session.participants.all() and c_session.remaining_seats() > 0:
                c_session.participants.add(applicant)
                send_sms(applicant.cell_phone, applicant.get_full_name(), 
                         c_session.course_name(), c_session.exam_start)
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
                                                                           show_score=f_exam.show_score, 
                                                                           session_total_seats =f_exam.session_total_seats)
                course_exam_session.participants.add(applicant)
                send_sms(applicant.cell_phone, applicant.get_full_name(), 
                         course_exam_session.course_name(), course_exam_session.exam_start)
                f_exam.increment_occupied()
                f_exam.course_sessions.add(course_exam_session)
            else:
                return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
            return Response(request.data, status=status.HTTP_201_CREATED)               









