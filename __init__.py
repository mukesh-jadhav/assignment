"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the CONFIG_TYPE environment variable
"""

import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configure the flask application instance
    CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Configure logging
    configure_logging()

    # Register error handlers
    register_error_handlers()

    return app


def register_error_handlers():
    pass


def configure_logging():
    pass
