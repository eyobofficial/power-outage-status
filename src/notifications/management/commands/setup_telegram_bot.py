from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from notifications.services import TelegramNotificationService
from notifications.models import TelegramSubscriber


class Command(BaseCommand):
    help = 'Setup Telegram bot and manage subscribers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Send a test message to verify bot is working',
        )
        parser.add_argument(
            '--add-subscriber',
            type=int,
            help='Add a new subscriber with the given chat ID',
        )
        parser.add_argument(
            '--remove-subscriber',
            type=int,
            help='Remove a subscriber with the given chat ID',
        )
        parser.add_argument(
            '--list-subscribers',
            action='store_true',
            help='List all active subscribers',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Username for the subscriber (optional)',
        )
        parser.add_argument(
            '--name',
            type=str,
            help='Name for the subscriber (optional)',
        )

    def handle(self, *args, **options):
        if not settings.TELEGRAM_BOT_TOKEN:
            raise CommandError(
                'TELEGRAM_BOT_TOKEN not configured. Please add it to your .env file.'
            )

        service = TelegramNotificationService()

        if options['test']:
            self.test_bot(service)
        elif options['add_subscriber']:
            self.add_subscriber(service, options)
        elif options['remove_subscriber']:
            self.remove_subscriber(service, options)
        elif options['list_subscribers']:
            self.list_subscribers()
        else:
            self.stdout.write(
                self.style.WARNING(
                    'No action specified. Use --help to see available options.'
                )
            )

    def test_bot(self, service):
        """Test the bot by sending a test message."""
        self.stdout.write('Testing Telegram bot...')
        
        # Get the first active subscriber for testing
        subscriber = TelegramSubscriber.objects.filter(is_active=True).first()
        
        if not subscriber:
            self.stdout.write(
                self.style.ERROR(
                    'No active subscribers found. Please add a subscriber first.'
                )
            )
            return

        success, message = service.send_test_message(subscriber.chat_id)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'Test message sent successfully to {subscriber.chat_id}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to send test message: {message}')
            )

    def add_subscriber(self, service, options):
        """Add a new subscriber."""
        chat_id = options['add_subscriber']
        username = options.get('username', '')
        name = options.get('name', '')

        subscriber = service.add_subscriber(chat_id, username, name)
        
        if subscriber:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Subscriber added successfully: {subscriber}'
                )
            )
            
            # Send a test message to verify
            success, message = service.send_test_message(chat_id)
            if success:
                self.stdout.write(
                    self.style.SUCCESS('Test message sent to verify subscription.')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Could not send test message: {message}')
                )
        else:
            self.stdout.write(
                self.style.ERROR('Failed to add subscriber.')
            )

    def remove_subscriber(self, service, options):
        """Remove a subscriber."""
        chat_id = options['remove_subscriber']
        
        success = service.remove_subscriber(chat_id)
        
        if success:
            self.stdout.write(
                self.style.SUCCESS(f'Subscriber {chat_id} removed successfully.')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to remove subscriber {chat_id}.')
            )

    def list_subscribers(self):
        """List all active subscribers."""
        subscribers = TelegramSubscriber.objects.filter(is_active=True)
        
        if not subscribers.exists():
            self.stdout.write('No active subscribers found.')
            return

        self.stdout.write('Active subscribers:')
        for subscriber in subscribers:
            self.stdout.write(
                f'  - {subscriber.chat_id}: {subscriber.name} (@{subscriber.username})'
            ) 