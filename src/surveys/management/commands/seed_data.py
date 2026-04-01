import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from surveys.models import AnswerChoice, Question, Survey


class Command(BaseCommand):
    help = 'Seed database with test survey data'

    def handle(self, *args, **kwargs):
        users = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f'user_{i}',
            )
            users.append(user)

        author = users[0]

        survey = Survey.objects.create(title='Test Survey: Vegetables', author=author)

        for q_order in range(1, 6):
            question = Question.objects.create(
                survey=survey,
                text=f'Question {q_order}: Do you like item {q_order}?',
                order=q_order,
                allow_custom_answer=random.random() < 0.3,
            )

            for c_order in range(1, 4):
                AnswerChoice.objects.create(question=question, text=f'Option {c_order}', order=c_order)

        self.stdout.write(self.style.SUCCESS('Test data created successfully'))
