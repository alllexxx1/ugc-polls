from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, AnswerChoice, Question, Survey, SurveySession
from .serializers import AnswerSubmitSerializer, QuestionSerializer


def get_user(request):
    user_id = request.headers.get('X-USER-ID')
    return User.objects.get(id=user_id)


class NextQuestionView(APIView):
    def get(self, request, survey_id):
        user = get_user(request)
        survey = get_object_or_404(Survey, id=survey_id, is_active=True)

        session, created = SurveySession.objects.get_or_create(
            user=user,
            survey=survey,
        )

        if session.is_completed:
            return Response(
                {'status': 'completed', 'message': 'You have already finished this survey'},
                status=status.HTTP_200_OK,
            )

        answered_question_ids = Answer.objects.filter(session=session).values_list('question_id', flat=True)

        next_question = (
            Question.objects
            .filter(survey=survey)
            .exclude(id__in=answered_question_ids)
            .select_related('survey')
            .prefetch_related('choices')
            .order_by('order')
            .first()
        )

        if not next_question:
            session.is_completed = True
            session.save(update_fields=['completed_at', 'is_completed'])
            return Response(
                {'status': 'completed', 'message': 'Survey is finished!'}, status=status.HTTP_200_OK
            )

        serializer = QuestionSerializer(next_question)
        return Response({'status': 'in_progress', 'question': serializer.data}, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, survey_id):
        user = get_user(request)
        survey = get_object_or_404(Survey, id=survey_id, is_active=True)
        session = get_object_or_404(SurveySession, user=user, survey=survey, is_completed=False)

        serializer = AnswerSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question_id']
        selected_option_id = serializer.validated_data.get('selected_option_id')
        custom_answer_text = serializer.validated_data.get('custom_answer_text', '').strip()

        question = get_object_or_404(Question, id=question_id, survey=survey)

        if Answer.objects.filter(session=session, question=question).exists():
            return Response(
                {'error': 'You have already answered this question'}, status=status.HTTP_400_BAD_REQUEST
            )

        if selected_option_id:
            selected_option = get_object_or_404(AnswerChoice, id=selected_option_id, question=question)
        else:
            selected_option = None
            if not question.allow_custom_answer:
                return Response(
                    {'error': 'The question creator does not allow users to enter their own answers'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        Answer.objects.create(
            session=session,
            question=question,
            choice=selected_option,
            custom_answer_text=custom_answer_text or None,
        )

        return self.get(request, survey_id)
