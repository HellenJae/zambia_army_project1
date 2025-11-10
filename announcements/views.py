from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Announcement

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def create_announcement(request):
    if request.user.role not in ['commander', 'officer']:
        return redirect('announcements:announcement_list')

    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        attachment = request.FILES.get('attachment')

        announcement = Announcement(
            title=title,
            message=message,
            created_by=request.user,
            attachment=attachment
        )

        # Handle voice note
        voice_data = request.POST.get('voice_note')
        if voice_data:
            format, audio_str = voice_data.split(';base64,')
            voice_file = ContentFile(base64.b64decode(audio_str), name="voice_note.webm")
            announcement.voice_note = voice_file

        announcement.save()
        return redirect('announcements:announcement_list')

    return render(request, 'announcements/create_announcement.html')