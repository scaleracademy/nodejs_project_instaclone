#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instaclone.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

  # web:
  #   build: ./instaclone
  #   command: python manage.py runserver 0.0.0.0:8000
  #   volumes:
  #     - ./instaclone/:/usr/src/instaclone/
  #   ports:
  #     - 8000:8000
  #   environment:
  #     - DEBUG=1
  #     - SECRET_KEY=alpha
  #     - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
  #     - POSTGRES_DB_NAME=instaclone_db
  #     - POSTGRES_USER=app_user
  #     - POSTGRES_PASSWORD=99DancingPips
  #     - POSTGRES_HOST=db
  #     - POSTGRES_PORT=5432
  #     - REDIS_URL=redis://localhost:6379