from . import views
from django.urls import path

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('user/', views.user_dashboard, name='user_dashboard'),
]
