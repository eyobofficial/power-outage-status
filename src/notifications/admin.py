from django.contrib import admin

from .models import TelegramSubscriber


@admin.register(TelegramSubscriber)
class TelegramSubscriberAdmin(admin.ModelAdmin):
    list_display = ("chat_id", "username", "name", "is_active")
    list_filter = ("is_active",)
    search_fields = ("username", "name")
