from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from power.models import PowerStatus
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update the power status (on/off) and send notifications'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            choices=['on', 'off'],
            required=True,
            help='Set power status to ON or OFF'
        )

    def handle(self, *args, **options):
        status = options['status']

        self.stdout.write(self.style.SUCCESS('Starting power status update...'))

        try:
            power_status, created = PowerStatus.objects.get_or_create(
                id=1,  # Use a single record for power status
                defaults={'is_on': False}
            )

            if created:
                self.stdout.write(self.style.WARNING('Created new power status record'))

            # Determine the new status
            new_status = status.lower() == 'on'
            self.stdout.write(f'Setting power status to: {"ON" if new_status else "OFF"}')

            # Update the status
            power_status.is_on = new_status
            power_status.save()

            # Output the result
            status_text = "ON" if new_status else "OFF"
            self.stdout.write(
                self.style.SUCCESS(f'Power status updated to: {status_text}')
            )

            # Convert timestamp to local timezone for display
            local_timestamp = timezone.localtime(power_status.last_updated)
            self.stdout.write(f'Timestamp: {local_timestamp}')

        except Exception as e:
            logger.error(f'Error updating power status: {e}')
            raise CommandError(f'Failed to update power status: {e}') 