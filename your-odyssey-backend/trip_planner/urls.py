from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacation_planner, name='vacation_planner'),
    path('comprehensive-plan/', views.comprehensive_plan_view, name='comprehensive_plan'),
    path('chat/', views.chat_view, name='chat'),
]