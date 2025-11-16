"""
Configuration file for Library Management System
Modify these settings according to your requirements
"""

import os

class Config:
    """Base configuration"""
    
    # Secret key for session management
    # IMPORTANT: Change this in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Borrowing settings
    BORROW_PERIOD_DAYS = 14  # Default borrowing period in days
    FINE_PER_DAY = 10  # Fine amount per day in rupees
    MAX_BOOKS_PER_USER = 5  # Maximum books a user can borrow at once
    
    # Book lost threshold
    LOST_BOOK_DAYS = 30  # Days after which an unreturned book is considered lost
    
    # Pagination
    BOOKS_PER_PAGE = 12
    RECORDS_PER_PAGE = 20


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_library.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
