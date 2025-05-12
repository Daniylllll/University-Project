from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout

from tests.models import Test
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required

from .models import TestRegistration, TestResult


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
    user = request.user
    full_name = user.full_name  # Получаем полное имя пользователя

    if user.role == 'teacher':  # Teacher's dashboard
        # Fetch the tests created by the teacher
        tests = Test.objects.filter(created_by=user)
        return render(request, 'dashboard.html', {
            'tests': tests,
            'role': 'teacher',
            'full_name': full_name,
        })

    elif user.role == 'student':  # Student's dashboard
        student_profile = user
        enrolled_tests = student_profile.tests.all()  # Тесты, на которые записан студент

        # Доступные тесты для присоединения через код
        available_tests = Test.objects.exclude(id__in=enrolled_tests.values('id'))

        return render(request, 'dashboard.html', {
            'tests': enrolled_tests,
            'available_tests': available_tests,
            'role': 'student',
            'full_name': full_name,
        })

    return redirect('login')


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


@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()  # Або інше відношення
    return render(request, 'tests/take_test.html', {
        'test': test,
        'questions': questions
    })


@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    correct_answers = 0

    for question in questions:
        selected = request.POST.get(f"question_{question.id}")
        if selected and int(selected) == question.correct_answer:
            correct_answers += 1

    student = request.user  # Пользователь, который сдавал тест

    TestRegistration.objects.create(
        test=test,
        student=student,
        score=correct_answers
    )

    context = {
        "test": test,
        "correct_answers": correct_answers,
        "total_questions": questions.count()
    }
    return render(request, "tests/test_result.html", context)
