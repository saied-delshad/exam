from rest_framework import serializers
from questions.models import QuestionModel

class QuestionSerializer(serializers.ModelSerializer):
    class Meta():
        model = QuestionModel
        exclude = ["created_at", "question_file", "correct_answer", "difficulty_level",
                    "numb_of_appeared", "correctly_answered_times"]
