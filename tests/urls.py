from django.urls import path
from . import views

# app_name = 'tests'  # This sets the namespace for the tests app


urlpatterns = [
    path('create/', views.create_test, name='create_test'),
    path('test/<int:id>/', views.test_detail, name='test_detail'),
    path('test/<int:id>/add_question/', views.add_question, name='add_question'),
]
