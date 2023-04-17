from rest_framework import serializers
from exam_sessions.models import SubjectExamSession, CourseExamSession, FreeExamSession, ExamResults

class SubjectSessionSerializer(serializers.ModelSerializer):

    class Meta():
        model = SubjectExamSession
        exclude = ["participants", "questions"]


class CourseSessionSerializer(serializers.ModelSerializer):

    class Meta():
        model = CourseExamSession
        fields = ['session_ref_number', 'course_name', 'exam_start', 'session_total_seats', 'remaining_seats']



class FreeSessionSerializer(serializers.ModelSerializer):

    class Meta():
        model = FreeExamSession
        fields = ['session_ref_number', 'exam_start', 'session_total_seats', 'remaining_seats']

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta():
        model = ExamResults
        exclude = ['created_at']

class ExamResultWriteSerializer(serializers.ModelSerializer):
    class Meta():
        model = ExamResults
        exclude = ['student', 'created_at', 'session_ref_number', 'score', 'is_passed']


class SessionsSerializer(serializers.Serializer):
    session_ref_number = serializers.CharField()
    exam_start = serializers.DateTimeField()
    remaining_seats = serializers.IntegerField()
    course = serializers.SerializerMethodField('get_course_name')


    def get_course_name(self, obj):
        if obj.session_ref_number.startswith('free'):
            return 'free'
        elif obj.session_ref_number.startswith('course'):
            return obj.get_course()