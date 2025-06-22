from django.db import models
from django_lifecycle import LifecycleModel, hook
import logging

logger = logging.getLogger(__name__)


class PowerStatus(LifecycleModel):
    is_on = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Power Status"
        verbose_name_plural = "Power Statuses"
    
    def __str__(self):
        status = "ON" if self.is_on else "OFF"
        return f"Power is {status} - {self.last_updated}"
    
    @hook('after_update', when='is_on', has_changed=True)
    def notify_power_status_change(self):
        """Send Telegram notification when power status changes."""
        try:
            # Import here to avoid circular imports
            from notifications.services import TelegramNotificationService

            service = TelegramNotificationService()
            service.send_power_status_notification(self)
                
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")