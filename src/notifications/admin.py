from django.contrib import admin

from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("name", "telegram_id")
    search_fields = ("name", "telegram_id")
    list_filter = ("created_at", "updated_at")
