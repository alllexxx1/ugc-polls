from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Survey(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    order = models.PositiveIntegerField()
    allow_custom_answer = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['survey', 'order']),
        ]

    def __str__(self):
        return self.text[:50]


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['question', 'order']),
        ]

    def __str__(self):
        return self.text[:50]


class SurveySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='survey_sessions')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'survey']),
            models.Index(fields=['survey', 'completed_at']),
        ]

    @property
    def duration(self):
        if self.completed_at and self.started_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

    def __str__(self):
        return f'{self.user} - {self.survey}'


class Answer(models.Model):
    session = models.ForeignKey(SurveySession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    choice = models.ForeignKey(
        AnswerChoice, null=True, blank=True, related_name='answers', on_delete=models.SET_NULL
    )
    custom_answer_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['session', 'question']]
        indexes = [
            models.Index(fields=['session', 'question']),
            models.Index(fields=['question', 'choice']),
            models.Index(fields=['question']),
        ]

    def __str__(self):
        return f'Answer {self.pk}'
