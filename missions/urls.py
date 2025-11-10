from django.urls import path
from . import views

app_name = 'missions'  # Optional, but good practice
urlpatterns = [
    path('', views.mission_list, name='mission_list'),
    path('complete/<int:mission_id>/', views.mark_completed, name='mark_completed'),
]
