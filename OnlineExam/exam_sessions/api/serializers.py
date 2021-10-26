from rest_framework import serializers
from exam_sessions.models import SubjectExamSession, CourseExamSession, ExamResults

class SubjectSessionSerializer(serializers.ModelSerializer):

    class Meta():
        model = SubjectExamSession
        exclude = ["participants", "questions"]


class CourseSessionSerializer(serializers.ModelSerializer):

    class Meta():
        model = CourseExamSession
        exclude = ['participants', 'questions']


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta():
        model = ExamResults
        exclude = ['created_at']

class ExamResultWriteSerializer(serializers.ModelSerializer):
    class Meta():
        model = ExamResults
        exclude = ['student', 'created_at', 'session_ref_number', 'score', 'is_passed']
