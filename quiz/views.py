from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Question, UserAnswer, AppRating
from .serializers import QuestionSerializer, UserAnswerSerializer, AppRatingSerializer
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Question, UserAnswer
from datetime import datetime
from django.shortcuts import get_object_or_404


# API Views
class QuestionListCreateView(generics.ListCreateAPIView):
    """
    Handles GET (list all questions) and POST (create new questions).
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


class QuestionView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    """
    Handles GET, PUT, PATCH, and DELETE for a single question.
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]


# Website Views

from django.shortcuts import redirect


def quiz_question(request, question_id):
    # Fetch the question by ID
    question = get_object_or_404(Question, id=question_id)

    # Calculate the progress percentage
    total_questions = Question.objects.count()
    progress_percentage = (
        (question_id / total_questions) * 100 if total_questions > 0 else 0
    )

    # Handle POST submission
    error_message = None
    if request.method == "POST":
        selected_answer = request.POST.get("answer")
        if not selected_answer:
            error_message = "Please select an answer."
        else:
            # Save the answer or process it here
            request.session[f"answer_{question_id}"] = selected_answer
            next_question_id = question_id + 1
            if next_question_id <= total_questions:
                return redirect("question", question_id=next_question_id)
            else:
                return redirect("results")

    # Get previous question ID
    previous_question_id = question_id - 1 if question_id > 1 else None

    return render(
        request,
        "question.html",
        {
            "question": question,
            "progress_percentage": progress_percentage,
            "error_message": error_message,
            "previous_question_id": previous_question_id,
            "year": datetime.now().year,
        },
    )


def quiz_result(request):
    """
    Handles displaying the quiz result.
    """
    user_id = request.session.session_key or "anonymous"
    answers = UserAnswer.objects.filter(user_id=user_id)
    frontend_score = answers.filter(
        answer="A", question__answer_type="frontend"
    ).count()
    backend_score = answers.filter(answer="B", question__answer_type="backend").count()
    total_questions = answers.count()

    if total_questions > 0:
        frontend_percentage = (frontend_score / total_questions) * 100
        backend_percentage = (backend_score / total_questions) * 100
    else:
        frontend_percentage = backend_percentage = 0

    if frontend_percentage >= 70:
        result_message = "You are most suitable for frontend development!"
    elif backend_percentage >= 70:
        result_message = "You are most suitable for backend development!"
    else:
        result_message = "You have a balanced skill set. Consider exploring both frontend and backend!"

    return render(
        request,
        "result.html",
        {
            "frontend_percentage": frontend_percentage,
            "backend_percentage": backend_percentage,
            "result_message": result_message,
        },
    )


def save_rating(request):
    """
    Save a user's app rating.
    """
    if request.method == "POST":
        rating = request.POST.get("rating")
        user_id = request.session.session_key or "anonymous"
        AppRating.objects.create(user_id=user_id, rating=rating)
        return HttpResponseRedirect("/result/")
