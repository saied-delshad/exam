from rest_framework import serializers
from exam_sessions.models import SubjectExamSession, CourseExamSession

class SubjectSessionSerializer(serializers.ModelSerializer):
    class Meta():
        model = SubjectExamSession
        exclude = ["participants", "questions"]
