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

4. Run migrations:
   ```bash
   cd src
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000`

## Configuration

The project uses environment variables for configuration. Create a `.env` file in the root directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

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

## Future Enhancements

- Real-time notifications for power status changes
- Integration with smart home devices
- Advanced analytics and reporting
- Mobile application support
- Multi-home support 