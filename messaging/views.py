from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Max
from .models import Message, Group
from accounts.models import CustomUser
from ai_summary.utils import generate_summary


# ==============================
# 📥 INBOX & SEARCH
# ==============================
@login_required
def inbox(request, user_id=None):

    query = request.GET.get('q', '').strip()
    selected_user = None
    messages_list = None
    no_search_results = False


    # ============================
    # 📨 1. Get All Conversation Partners
    # ============================

    conversations = (
        Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        )
        .values('sender', 'recipient')
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
    )


    user_ids = {
        convo['sender']
        if convo['sender'] != request.user.id
        else convo['recipient']
        for convo in conversations
    }


    users = CustomUser.objects.filter(id__in=user_ids)



    # ============================
    # 💬 2. Latest Message Preview
    # ============================

    latest_messages = {}

    for user in users:

        last_msg = (
            Message.objects.filter(
                (Q(sender=request.user) & Q(recipient=user)) |
                (Q(sender=user) & Q(recipient=request.user))
            )
            .order_by('-timestamp')
            .first()
        )

        latest_messages[user.id] = (
            last_msg.content
            if last_msg
            else ""
        )



    # ============================
    # 🔍 3. Search Users
    # ============================

    if query:

        searched_users = CustomUser.objects.filter(

            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(man_number__icontains=query)

        ).exclude(id=request.user.id)


        if searched_users.exists():

            users = searched_users

        else:

            users = []
            no_search_results = True




    # ============================
    # 💌 4. Load Conversation
    # ============================

    if user_id:

        selected_user = get_object_or_404(
            CustomUser,
            id=user_id
        )


        messages_list = Message.objects.filter(

            (Q(sender=request.user) & Q(recipient=selected_user)) |
            (Q(sender=selected_user) & Q(recipient=request.user))

        ).order_by('timestamp')




    # ============================
    # ✉️ 5. Send Message
    # ============================

    if request.method == "POST" and user_id:


        other_user = get_object_or_404(
            CustomUser,
            id=user_id
        )


        content = request.POST.get(
            'message',
            ''
        ).strip()



        message = Message(
            sender=request.user,
            recipient=other_user
        )


        # Text message

        if content:

            message.content = content



        # Attachments

        attachments = [
            'attachment_doc',
            'attachment_photo',
            'attachment_audio',
            'voice_note'
        ]


        for field in attachments:

            if field in request.FILES:

                setattr(
                    message,
                    field,
                    request.FILES[field]
                )



        # Save message

        if content or any(
            field in request.FILES
            for field in attachments
        ):

            message.save()



            # ============================
            # 🤖 ORION AI UPDATE
            # ============================

            # Update receiver's AI briefing

            generate_summary(other_user)



        return redirect(
            'messaging:conversation_detail',
            user_id=other_user.id
        )




    # ============================
    # 🖼️ 6. Render
    # ============================

    return render(
        request,
        'messaging/inbox.html',
        {

            'users': users,

            'latest_messages': latest_messages,

            'query': query,

            'selected_user': selected_user,

            'messages': messages_list,

            'no_search_results': no_search_results,

        }
    )

# ==============================
# 💬 CONVERSATION DETAIL
# ==============================
@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    # Get messages between both users
    messages_list = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user))
        | (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    # ---- Sending a new message ----
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        message = Message(sender=request.user, recipient=other_user)

        # Attachments
        for field in ['attachment_doc', 'attachment_photo', 'attachment_audio', 'voice_note']:
            if field in request.FILES:
                setattr(message, field, request.FILES[field])

        if content:
            message.content = content

        if content or any(field in request.FILES for field in ['attachment_doc', 'attachment_photo', 'attachment_audio', 'voice_note']):
            message.save()

        return redirect('messaging:conversation_detail', user_id=other_user.id)

    # ---- Sidebar: show all users you’ve chatted with ----
    conversations = (
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values('sender', 'recipient')
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
    )

    user_ids = {
        convo['sender'] if convo['sender'] != request.user.id else convo['recipient']
        for convo in conversations
    }

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
        'messages': messages_list,
    })


# ==============================
# 🗑️ DELETE SINGLE MESSAGE
# ==============================
@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id)
    if msg.sender == request.user:
        msg.delete()
        messages.success(request, "Message deleted successfully.")
    else:
        messages.error(request, "You cannot delete this message.")
    return redirect(request.META.get('HTTP_REFERER', 'messaging:inbox'))


# ==============================
# 👥 GROUP CREATION
# ==============================
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


# ==============================
# 🚮 CLEAR ALL MESSAGES
# ==============================
@login_required
def clear_all_messages(request):
    Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).delete()
    return redirect('messaging:inbox')


# ==============================
# 💬 DELETE WHOLE CONVERSATION
# ==============================
@login_required
def delete_conversation(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        Message.objects.filter(
            sender__in=[request.user, other_user],
            recipient__in=[request.user, other_user]
        ).delete()
        messages.success(request, f"Conversation with {other_user.first_name} deleted!")
        return redirect('messaging:inbox')

    return redirect('messaging:conversation_detail', user_id=user_id)


# ==============================
# ✅ DELETE SELECTED MESSAGES
# ==============================
@login_required
def delete_selected_messages(request, user_id):
    other_user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        message_ids_str = request.POST.get('message_ids[]')  # e.g. "26,27,28"
        if message_ids_str:
            message_ids = [int(mid) for mid in message_ids_str.split(',') if mid.isdigit()]
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
