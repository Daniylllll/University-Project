from django.db import models

from app import settings


class Test(models.Model):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=8, unique=True)  # Код для доступу до тесту

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, default="")
    answer_1 = models.CharField(max_length=200, default="")  # Новый ответ с дефолтным значением
    answer_2 = models.CharField(max_length=200, default="")
    answer_3 = models.CharField(max_length=200, default="")
    answer_4 = models.CharField(max_length=200, default="")
    correct_answer = models.IntegerField(choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3'), (4, 'Answer 4')],
                                         default=1)

    def __str__(self):
        return self.question_text


