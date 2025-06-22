from django.shortcuts import render
from django.utils import timezone
from .models import PowerStatus


def home(request):
    """Display the current power status on the home page."""
    try:
        # Get the current power status
        power_status = PowerStatus.objects.get(id=1)
        
        # Convert timestamp to local timezone for display
        local_timestamp = timezone.localtime(power_status.last_updated)
        formatted_timestamp = local_timestamp.strftime("%H:%M %b %d, %Y")
        
        context = {
            'power_status': power_status,
            'formatted_timestamp': formatted_timestamp,
            'status_text': "ON" if power_status.is_on else "OFF",
            'status_emoji': "🟢" if power_status.is_on else "🔴",
        }
        
    except PowerStatus.DoesNotExist:
        # If no power status record exists, show default values
        context = {
            'power_status': None,
            'formatted_timestamp': "Never",
            'status_text': "UNKNOWN",
            'status_emoji': "⚪",
        }
    
    return render(request, 'power/home.html', context) 