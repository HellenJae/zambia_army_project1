from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Group
from accounts.models import CustomUser
from django.db.models import Q, Max
from django.core.files.base import ContentFile
import base64
import re

@login_required
def inbox(request, user_id=None):
    query = request.GET.get('q', '').strip()
    selected_user = None
    messages_list = None
    no_search_results = False

    # Load all conversation partners
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values('sender', 'recipient')
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
    )

    user_ids = set()
    for convo in conversations:
        if convo['sender'] != request.user.id:
            user_ids.add(convo['sender'])
        if convo['recipient'] != request.user.id:
            user_ids.add(convo['recipient'])

    users = CustomUser.objects.filter(id__in=user_ids)

    # Latest message preview
    latest_messages = {}
    for user in users:
        last_msg = (
            Message.objects.filter(
                (Q(sender=request.user) & Q(recipient=user))
                | (Q(sender=user) & Q(recipient=request.user))
            ).order_by('-timestamp').first()
        )
        latest_messages[user.id] = last_msg.content if last_msg else ""

    # Handle search without removing the conversation list
    searched_users = []
    if query:
        searched_users = users.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(man_number__icontains=query)
            | Q(username__icontains=query)
        )
        if not searched_users.exists():
            no_search_results = True
    else:
        searched_users = users  # show all if no query

    # 💬 Load specific chat if user_id provided
    if user_id:
        selected_user = get_object_or_404(CustomUser, id=user_id)
        messages_list = Message.objects.filter(
            (Q(sender=request.user) & Q(recipient=selected_user))
            | (Q(sender=selected_user) & Q(recipient=request.user))
        ).order_by('timestamp')

    # Sending a message
    if request.method == "POST" and user_id:
        other_user = get_object_or_404(CustomUser, id=user_id)
        content = request.POST.get('message', '').strip()
        message = Message.objects.create(
            sender=request.user,
            recipient=other_user,
            content=content if content else None,
        )

        # attachments
        for file_field in ['attachment_doc', 'attachment_photo', 'attachment_audio', 'voice_note']:
            if file_field in request.FILES:
                setattr(message, file_field, request.FILES[file_field])

        message.save()
        return redirect('messaging:conversation_detail', user_id=other_user.id)

    return render(request, 'messaging/inbox.html', {
        'users': users,
        'searched_users': searched_users,
        'latest_messages': latest_messages,
        'query': query,
        'selected_user': selected_user,
        'messages': messages_list,
        'no_search_results': no_search_results,
    })


@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    # Messages between logged-in user and the selected user
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    # Send a new message
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        attachment_doc = request.FILES.get('attachment_doc')
        attachment_photo = request.FILES.get('attachment_photo')
        attachment_audio = request.FILES.get('attachment_audio')
        voice_note_file = request.FILES.get('voice_note')

        message = Message(sender=request.user, recipient=other_user, read=False)

        if content:
            message.content = content
        if attachment_doc:
            message.attachment_doc = attachment_doc
        if attachment_photo:
            message.attachment_photo = attachment_photo
        if attachment_audio:
            message.attachment_audio = attachment_audio
        if voice_note_file:
            message.voice_note = voice_note_file

        if content or attachment_doc or attachment_photo or attachment_audio or voice_note_file:
            message.save()

        return redirect('messaging:conversation_detail', user_id=other_user.id)

    # Get all conversation users for sidebar
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values('sender', 'recipient')
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
    )

    user_ids = set()
    for convo in conversations:
        if convo['sender'] != request.user.id:
            user_ids.add(convo['sender'])
        if convo['recipient'] != request.user.id:
            user_ids.add(convo['recipient'])

    users = CustomUser.objects.filter(id__in=user_ids)

    latest_messages = {}
    for user in users:
        last_msg = (
            Message.objects.filter(
                (Q(sender=request.user) & Q(recipient=user))
                | (Q(sender=user) & Q(recipient=request.user))
            ).order_by('-timestamp').first()
        )
        latest_messages[user.id] = last_msg.content if last_msg else ""

    return render(request, 'messaging/conversation_detail.html', {
        'users': users,
        'latest_messages': latest_messages,
        'selected_user': other_user,
        'messages': messages,
    })


@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    if msg.sender == request.user:  # Only the sender can delete their message
        msg.delete()
        messages.success(request, "Message deleted successfully.")
    else:
        messages.error(request, "You cannot delete this message.")
    return redirect(request.META.get('HTTP_REFERER', 'messaging:inbox'))


@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        members_ids = request.POST.getlist('members')
        members = CustomUser.objects.filter(id__in=members_ids)

        group = Group.objects.create(name=name)
        group.members.set(members)
        group.save()

        return redirect('messaging:group_chat', group_id=group.id)

    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, 'messaging/create_group.html', {'users': users})
@login_required
def clear_all_messages(request):
    Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).delete()
    return redirect('messaging:inbox')



@login_required
def delete_conversation(request, user_id):
    """
    Delete all messages between the current user and another user.
    Triggered from chat header three-dot menu.
    """
    other_user = get_object_or_404(CustomUser, id=user_id)  # ✅ use CustomUser

    if request.method == "POST":
        # Delete all messages where sender and recipient are the two users
        Message.objects.filter(
            sender__in=[request.user, other_user],
            recipient__in=[request.user, other_user]  # ✅ recipient, not receiver
        ).delete()
        messages.success(request, f"Conversation with {other_user.first_name} deleted!")
        return redirect('messaging:inbox')

    return redirect('messaging:conversation_detail', user_id=user_id)

@login_required
def delete_selected_messages(request, user_id):
    """
    Delete selected messages in a conversation.
    Expects POST with a list of message IDs named 'message_ids[]'.
    """
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        message_ids_str = request.POST.get('message_ids[]')  # Single string like '26,27'
        if message_ids_str:
            # Convert to list of integers
            message_ids = [int(mid) for mid in message_ids_str.split(',')]
            
            Message.objects.filter(
                id__in=message_ids,
                sender__in=[request.user, other_user],
                recipient__in=[request.user, other_user]
            ).delete()
            messages.success(request, "Selected messages deleted!")
        else:
            messages.error(request, "No messages selected to delete.")

        return redirect('messaging:conversation_detail', user_id=user_id)

    return redirect('messaging:conversation_detail', user_id=user_id)
