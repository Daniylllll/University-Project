from django import forms
from .models import Test, Question


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'subject']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct_answer']
        widgets = {
            'correct_answer': forms.RadioSelect(),
        }

