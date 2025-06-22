import logging
import requests
from django.conf import settings
from django.utils import timezone
from .models import TelegramSubscriber

logger = logging.getLogger(__name__)


class TelegramNotificationService:
    """Service for sending Telegram notifications about power status changes."""
    
    def __init__(self):
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}" if self.bot_token else None
    
    def send_power_status_notification(self, power_status, previous_value=None):
        """Send notification about power status change to all active subscribers."""
        if not self.bot_token:
            logger.warning("Telegram bot token not configured. Skipping notification.")
            return
        
        try:
            # Get all active subscribers
            subscribers = TelegramSubscriber.objects.filter(is_active=True)
            
            if not subscribers.exists():
                logger.info("No active Telegram subscribers found.")
                return
            
            # Prepare the message
            message = self._prepare_notification_message(power_status)
            
            # Send to all subscribers
            for subscriber in subscribers:
                self._send_message_to_subscriber(subscriber, message)
                
        except Exception as e:
            logger.error(f"Error sending power status notification: {e}")
    
    def _prepare_notification_message(self, power_status) -> str:
        """Prepare the notification message based on power status."""
        status = "🟢 ON" if power_status.is_on else "🔴 OFF"
        timestamp = power_status.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"⚡ Power Status: {status}\n"
        message += f"Time: {timestamp}\n"
        
        return message
    
    def _send_message_to_subscriber(self, subscriber: TelegramSubscriber, message: str):
        """Send message to a specific subscriber using synchronous requests."""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': subscriber.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                logger.info(f"Notification sent to subscriber {subscriber.chat_id}")
            else:
                logger.error(f"Telegram API error for subscriber {subscriber.chat_id}: {result.get('description')}")
                self._handle_telegram_error(subscriber, result.get('description', ''))
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to subscriber {subscriber.chat_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error sending message to subscriber {subscriber.chat_id}: {e}")
    
    def _handle_telegram_error(self, subscriber: TelegramSubscriber, error_description: str):
        """Handle Telegram API errors and deactivate subscribers if necessary."""
        error_lower = error_description.lower()
        if "chat not found" in error_lower or "blocked" in error_lower or "user deactivated" in error_lower:
            subscriber.is_active = False
            subscriber.save()
            logger.warning(f"Deactivated subscriber {subscriber.chat_id} due to Telegram error: {error_description}")
    
    def add_subscriber(self, chat_id: int, username: str = "", name: str = ""):
        """Add a new Telegram subscriber."""
        try:
            subscriber, created = TelegramSubscriber.objects.get_or_create(
                chat_id=chat_id,
                defaults={
                    'username': username,
                    'name': name,
                    'is_active': True
                }
            )
            
            if not created:
                # Update existing subscriber
                subscriber.username = username
                subscriber.name = name
                subscriber.is_active = True
                subscriber.save()
            
            logger.info(f"Subscriber {'added' if created else 'updated'}: {chat_id}")
            return subscriber
            
        except Exception as e:
            logger.error(f"Error adding subscriber {chat_id}: {e}")
            return None
    
    def remove_subscriber(self, chat_id: int):
        """Remove a Telegram subscriber."""
        try:
            subscriber = TelegramSubscriber.objects.get(chat_id=chat_id)
            subscriber.is_active = False
            subscriber.save()
            logger.info(f"Subscriber deactivated: {chat_id}")
            return True
        except TelegramSubscriber.DoesNotExist:
            logger.warning(f"Subscriber not found: {chat_id}")
            return False
        except Exception as e:
            logger.error(f"Error removing subscriber {chat_id}: {e}")
            return False
    
    def send_test_message(self, chat_id: int):
        """Send a test message to verify the bot is working."""
        if not self.bot_token:
            return False, "Telegram bot token not configured"
        
        try:
            message = "🧪 Test Message\n\nThis is a test notification from your Power Status Tracker bot. If you receive this message, the bot is working correctly!"
            
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                return True, "Test message sent successfully"
            else:
                return False, f"Telegram API error: {result.get('description')}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"
    
    def get_bot_info(self):
        """Get information about the bot."""
        if not self.bot_token:
            return None, "Telegram bot token not configured"
        
        try:
            url = f"{self.base_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            if result.get('ok'):
                return result.get('result'), None
            else:
                return None, f"Telegram API error: {result.get('description')}"
                
        except requests.exceptions.RequestException as e:
            return None, f"Request error: {e}"
        except Exception as e:
            return None, f"Unexpected error: {e}" 