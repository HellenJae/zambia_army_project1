from django.urls import path
from . import views  # Import all views from messaging app

app_name = 'messaging'

urlpatterns = [
    # Inbox & conversation
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation_detail, name='conversation_detail'),

    # Delete messages
   
    path('conversation/<int:user_id>/delete/', views.delete_conversation, name='delete_conversation'),
    path('clear_all_messages/', views.clear_all_messages, name='clear_all_messages'),
    path('conversation/<int:user_id>/delete-selected/', views.delete_selected_messages, name='delete_selected_messages'),

    # Group creation
    path('create-group/', views.create_group, name='create_group'),
]
