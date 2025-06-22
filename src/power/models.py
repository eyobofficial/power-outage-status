from django.db import models

from django_lifecycle import LifecycleModel, hook


class PowerStatus(LifecycleModel):
    is_on = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Power Status"
        verbose_name_plural = "Power Statuses"