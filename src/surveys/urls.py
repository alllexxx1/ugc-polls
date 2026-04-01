from django.urls import path

from .views import NextQuestionView

urlpatterns = [
    path('survey/<int:survey_id>/next-question/', NextQuestionView.as_view()),
]
