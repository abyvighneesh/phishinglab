"""
Vercel serverless entry point for PhishLab
"""
import sys
import os

# Set production environment
os.environ['FLASK_ENV'] = 'production'

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    
    # This is the entry point for Vercel
    # Vercel expects a WSGI application object named 'app'
    
except ImportError as e:
    # Fallback error handler
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return {
            'error': 'Failed to import main Flask app',
            'details': str(e)
        }, 500
