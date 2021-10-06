from rest_framework import serializers
from exam_sessions.models import SubjectExamSession, CourseExamSession, ExamResults

class SubjectSessionSerializer(serializers.ModelSerializer):
    class Meta():
        model = SubjectExamSession
        exclude = ["participants", "questions"]


class ExamResultSerializer(serializers.ModelSerializer):
    class Meta():
        model = ExamResults
        exclude = ['course_exam_session', 'subject_exam_session', 'created_at', 'score', 'is_passed']
