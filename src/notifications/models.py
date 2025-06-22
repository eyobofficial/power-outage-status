from django.db import models


class TelegramSubscriber(models.Model):
    chat_id = models.BigIntegerField(unique=True, help_text="Telegram chat ID")
    username = models.CharField(max_length=100, blank=True, help_text="Telegram username")
    name = models.CharField(max_length=100, blank=True, help_text="User's name")
    is_active = models.BooleanField(default=True, help_text="Whether to send notifications to this subscriber")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Telegram Subscriber"
        verbose_name_plural = "Telegram Subscribers"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.chat_id}"