from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_dashboard, name='dashboard_admin'),
    path('officer/', views.officer_dashboard, name='dashboard_officer'),
    path('soldier/', views.soldier_dashboard, name='dashboard_soldier'),
    path('profile/', dashboard_views.profile_update, name='profile'),  
    path('profile/update/', dashboard_views.profile_update, name='profile_update'),
]
