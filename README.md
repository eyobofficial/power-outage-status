# Power Status Tracker

A Django-based web application for tracking and monitoring the electric power status of your home. This application runs on a home Ubuntu server to provide real-time power status information and historical data analysis.

## Project Overview

The Power Status Tracker is designed to monitor and log electrical power status information from your home's electrical system. It provides a web interface to view current power status, historical trends, and power consumption patterns.

## Features

- Real-time power status monitoring
- Historical data tracking and visualization
- Web-based dashboard interface
- RESTful API for data access
- SQLite database for data storage
- **Telegram notifications** for power status changes

## Project Structure

```
power-status/
├── src/                    # Django project source code
│   ├── power_status/       # Main Django project
│   ├── apps/              # Django applications
│   └── manage.py          # Django management script
├── requirements.in         # pip-tools requirements input
├── pyproject.toml         # Project configuration
├── .gitignore            # Git ignore rules
├── LICENSE               # MIT License
└── README.md             # This file
```

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default)
- **Dependency Management**: pip-tools
- **Python Version**: 3.11+
- **Server**: Django Development Server
- **Environment Management**: python-decouple
- **Notifications**: Telegram Bot API

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd power-status
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pip-tools
   pip-compile requirements.in
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   # Create .env file in the root directory
   cat > .env << EOF
   DEBUG=True
   SECRET_KEY=your-secret-key-change-this-in-production
   ALLOWED_HOSTS=*
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
   EOF
   ```

5. Run migrations:
   ```bash
   cd src
   python manage.py migrate
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://localhost:8000`

## Configuration

The project uses `python-decouple` to manage environment variables from a `.env` file. Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=*

# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
```

### Environment Variables

- **DEBUG**: Set to `True` for development, `False` for production
- **SECRET_KEY**: Django secret key for security (change in production)
- **ALLOWED_HOSTS**: Comma-separated list of allowed hostnames (use `*` to allow all hosts)
- **TELEGRAM_BOT_TOKEN**: Your Telegram bot token for notifications (optional)

## Telegram Notifications Setup

### 1. Create a Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### 2. Configure the Bot Token

Add your bot token to the `.env` file:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 3. Add Subscribers

Use the management command to add subscribers:

```bash
# Add a subscriber (replace with actual chat ID)
python src/manage.py setup_telegram_bot --add-subscriber 123456789 --username your_username --name "Your Name"

# Test the bot
python src/manage.py setup_telegram_bot --test

# List all subscribers
python src/manage.py setup_telegram_bot --list-subscribers

# Remove a subscriber
python src/manage.py setup_telegram_bot --remove-subscriber 123456789
```

### 4. Get Your Chat ID

To find your chat ID:
1. Start a conversation with your bot
2. Send any message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for the `chat.id` field in the response

### 5. Automatic Notifications

Once configured, the system will automatically send notifications when:
- Power status changes from ON to OFF or vice versa

## Development

### Adding Dependencies

To add new dependencies, edit `requirements.in` and then run:
```bash
pip-compile requirements.in
```

### Running Tests

```bash
cd src
python manage.py test
```

### Code Style

The project follows PEP 8 style guidelines. Use a linter like `flake8` or `black` for code formatting.

### Database Management

```bash
# Create migrations
python src/manage.py makemigrations

# Apply migrations
python src/manage.py migrate

# Create superuser
python src/manage.py createsuperuser

# Access Django admin
# Visit http://localhost:8000/admin/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Architecture

The project follows a modular Django architecture:

- **Models**: Define data structures for power status tracking
- **Views**: Handle HTTP requests and responses
- **Templates**: Provide the user interface
- **API**: RESTful endpoints for data access
- **Management Commands**: Custom Django commands for data collection
- **Services**: Telegram notification service for real-time alerts

## Future Enhancements

- Real-time notifications for power status changes ✅
- Integration with smart home devices
- Advanced analytics and reporting
- Mobile application support
- Multi-home support 