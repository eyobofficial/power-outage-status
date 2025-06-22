from django.contrib import admin

from .models import PowerStatus


@admin.register(PowerStatus)
class PowerStatusAdmin(admin.ModelAdmin):
    list_display = ("is_on", "last_updated")
    list_filter = ("is_on",)

