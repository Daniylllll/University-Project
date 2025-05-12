from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from tests.models import Test


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'

    tests = models.ManyToManyField(Test, through='TestRegistration', related_name='students')

    def __str__(self):
        return self.full_name


class TestRegistration(models.Model):
    student = models.ForeignKey(CustomUser, related_name='test_registrations', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='registrations', on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'test')

    def __str__(self):
        return f'{self.student.full_name} - {self.test.title}'


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

