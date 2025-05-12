from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import TestRegistration, TestResult, CustomUser
from .models import Test, Question
from .forms import TestForm, QuestionForm
import random
import string


def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Генерация кода длиной 8 символов


@login_required
def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.created_by = request.user  # ← ВАЖНО!
            test.code = generate_unique_code()  # Генерируем уникальный код для теста

            # Проверка уникальности кода
            while Test.objects.filter(code=test.code).exists():
                test.code = generate_unique_code()  #
            test.save()
            return redirect('test_detail', test.id)
    else:
        form = TestForm()
    return render(request, 'tests/create_test.html', {'form': form})


@login_required
def test_detail(request, id):
    test = get_object_or_404(Test, id=id)  # Получаем тест по ID
    user = request.user

    # Проверяем, является ли пользователь учителем или студентом
    is_teacher = user.role == 'teacher'

    student_result = None
    student_results = []

    # Если пользователь студент
    if not is_teacher:
        student_registration = TestRegistration.objects.filter(test=test, student=user).first()
        if student_registration:
            student_result = student_registration.score  # Результат студента
    else:
        # Если пользователь учитель, показываем результаты всех студентов
        student_results = TestRegistration.objects.filter(test=test)

    return render(request, 'tests/test_detail.html', {
        'test': test,
        'student_result': student_result,  # Для студента — его результат
        'student_results': student_results,  # Для учителя — все результаты студентов
        'is_teacher': is_teacher,  # Флаг для отображения информации в зависимости от роли
    })



@login_required
def add_question(request, id):
    test = get_object_or_404(Test, pk=id)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.test = test  # Устанавливаем тест для вопроса
            question.save()
            return redirect('test_detail', test.id)
    else:
        form = QuestionForm()

    return render(request, 'tests/add_question.html', {'form': form, 'test': test})
