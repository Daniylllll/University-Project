from django.urls import path
from .views import register_view, login_view, logout_view, dashboard_view, join_test_by_code, take_test, submit_test


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('join_test_by_code/', join_test_by_code, name='join_test_by_code'),
    path('test/<int:test_id>/take/', take_test, name='take_test'),
    path('test/<int:test_id>/submit/', submit_test, name='submit_test'),
]
