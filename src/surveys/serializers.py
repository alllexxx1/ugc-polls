from rest_framework import serializers

from .models import AnswerChoice, Question


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'order', 'choices']


class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option_id = serializers.IntegerField(required=False, allow_null=True)
    custom_answer_text = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        if not data.get('selected_option_id') and not data.get('custom_answer_text'):
            raise serializers.ValidationError('Choose an option for the option list or enter your answer')
        if data.get('selected_option_id') and data.get('custom_answer_text'):
            raise serializers.ValidationError(
                'You cannot enter your answer and choose an option at the same time'
            )
        return data
