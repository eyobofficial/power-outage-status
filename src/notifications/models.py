from django.db import models


class Subscriber(models.Model):
    name = models.CharField(max_length=255)
    telegram_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"