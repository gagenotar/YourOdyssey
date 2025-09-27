from django.urls import path
from . import views

app_name = 'trip_planner'

urlpatterns = [
    path('', views.home, name='home'),
    path('plan/', views.plan_trip, name='plan_trip'),
    path('weather/', views.get_weather, name='get_weather'),
    path('comprehensive-plan/', views.comprehensive_plan, name='comprehensive_plan'),
]