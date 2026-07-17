from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notification_list(request):
    filter_type = request.GET.get('type', 'all')

    notifications = Notification.objects.filter(user=request.user).order_by('-id')

    if filter_type == 'trade':
        notifications = notifications.filter(notification_type='trade')
    elif filter_type == 'stock':
        notifications = notifications.filter(notification_type='stock')

    notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications/list.html', {
        'notifications': notifications,
        'filter_type': filter_type,
    })