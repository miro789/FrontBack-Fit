from django.urls import path
from django.shortcuts import redirect
from .views import (
    QuestionListCreateView,
    QuestionView,
    quiz_result,
    quiz_question,
    save_rating,
)

urlpatterns = [
    # API Endpoints
    path(
        "api/questions/", QuestionListCreateView.as_view(), name="question-list-create"
    ),
    path("api/questions/<int:pk>/", QuestionView.as_view(), name="question-detail"),
    # Main Website
    path(
        "", lambda request: redirect("question", question_id=1), name="quiz-home"
    ),  # Default route
    path(
        "question/<int:question_id>/", quiz_question, name="question"
    ),  # URL for question view
    path("result/", quiz_result, name="quiz-result"),
    path("rate-app/", save_rating, name="rate-app"),
]
