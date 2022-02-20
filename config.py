import os
from dotenv import load_dotenv

load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    MIN_NBR_PKTS = 1
    MAX_NBR_PKTS = 10
    WAIT_TIME = 1

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='A very terrible secret key.')
    CELERY_BROKER_URL: str = 'redis://127.0.0.1:6379/0'
    RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

    WEBHOOK_RECEIVER_URL = "http://127.0.0.1:5001/write"
    RESOURCE_DIR = r"data_dumps"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
