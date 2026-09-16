from django.urls import path
from . import views

app_name = 'ai_summary'

urlpatterns = [
    path('dashboard/', views.ai_summary_dashboard, name='dashboard'),
    path('panel/', views.ai_panel, name='panel'),
    path('meta/', views.meta_assistant, name='meta'),
]