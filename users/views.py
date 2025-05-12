from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout

from tests.models import Test
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import TestRegistration, CustomUser

import logging

logger = logging.getLogger(__name__)


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # или куда нужно
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    if request.user.role == 'teacher':  # Teacher's dashboard
        # Fetch the tests created by the teacher
        tests = Test.objects.filter(created_by=request.user)
        return render(request, 'dashboard.html', {'tests': tests, 'role': 'teacher'})

    elif request.user.role == 'student':  # Student's dashboard
        student_profile = request.user
        enrolled_tests = student_profile.tests.all()  # Тесты, на которые записан студент

        # Доступные тесты для присоединения через код
        available_tests = Test.objects.exclude(id__in=enrolled_tests.values('id'))

        return render(request, 'dashboard.html', {
            'tests': enrolled_tests,
            'available_tests': available_tests,
            'role': 'student'
        })

    return redirect('login')  # In case of an invalid role or any other issue


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    # Створюємо запис для студента, якщо його ще немає
    if not TestRegistration.objects.filter(test=test, student=request.user).exists():
        TestRegistration.objects.create(test=test, student=request.user)

    return render(request, 'take_test.html', {'test': test})


@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    if request.method == "POST":
        score = 0

        # Проходим по всем вопросам теста
        for question in test.questions.all():
            selected_answer = request.POST.get(f"question_{question.id}")
            if selected_answer and int(selected_answer) == question.correct_answer:
                score += 1

        # Обновляем или создаем запись о результатах студента
        registration, created = TestRegistration.objects.get_or_create(test=test, student=request.user)
        registration.score = score
        registration.save()

        messages.success(request, f"You have completed the test! Your score is {score}.")
        return redirect('test_results', test_id=test.id)


@login_required
def join_test_by_code(request):
    if request.method == "POST":
        test_code = request.POST.get("test_code")

        # Ищем тест по коду
        test = Test.objects.filter(code=test_code).first()

        if test:
            # Проверяем, не присоединился ли студент к тесту
            if not TestRegistration.objects.filter(test=test, student=request.user).exists():
                # Добавляем студента в тест
                TestRegistration.objects.create(test=test, student=request.user)
                messages.success(request, "You have successfully joined the test!")
                return redirect('take_test', test_id=test.id)
            else:
                messages.warning(request, "You are already enrolled in this test.")
                return redirect('dashboard')
        else:
            messages.error(request, "Test with this code does not exist.")
            return redirect('dashboard')
    else:
        return redirect('dashboard')
