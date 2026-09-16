from django.contrib import admin
from django.urls import path, include
from main import views as main_views
from accounts import views as accounts_views
from messaging import views as messaging_views
from dashboard import views as dashboard_views  # make sure profile_update is here
from django.conf import settings
from django.conf.urls.static import static

app_name = 'messaging'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home
    path('', main_views.home, name='home'),
    path('slash/', main_views.slash, name='slash'),

    # Accounts
    path('register/', accounts_views.register_view, name='register'),
    path('login/', accounts_views.login_view, name='login'),
    path('logout/', accounts_views.logout_view, name='logout'),

    # Dashboards
    
    path('dashboard/', accounts_views.dashboard, name='dashboard'),
    path('dashboard/soldier/', dashboard_views.soldier_dashboard, name='dashboard_soldier'),
    path('dashboard/officer/', dashboard_views.officer_dashboard, name='dashboard_officer'),
    path('dashboard/commander/', dashboard_views.commander_dashboard, name='dashboard_commander'),
    path('dashboard/admin/', dashboard_views.admin_dashboard, name='dashboard_admin'),

    # Messaging
   path('messages/', include(('messaging.urls', 'messaging'), namespace='messaging')),

    # Missions & Announcements
    path('missions/', include(('missions.urls', 'missions'), namespace='missions')),
    path('announcements/', include('announcements.urls', namespace='announcements')),

    path('ai/', include('ai_security.urls')),
    path('ai/', include('ai_summary.urls')),

    # Profile
    path('profile/', dashboard_views.profile_update, name='profile'),          # display profile page / GET
    path('profile/update/', dashboard_views.profile_update, name='profile_update'),  # handle POST
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
