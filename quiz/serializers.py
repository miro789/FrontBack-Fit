from rest_framework import serializers
from .models import Question, UserAnswer, AppRating


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class AppRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppRating
        fields = "__all__"
