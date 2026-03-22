"""
Vercel serverless entry point for PhishLab
This file handles all requests from Vercel
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set production environment
os.environ['FLASK_ENV'] = 'production'

try:
    # Import the Flask app from app.py
    from app import app
    
    # Export the app for Vercel
    # Vercel will call this as a WSGI application
    handler = app
    
except Exception as e:
    # If there's an import error, create a minimal error handler
    import json
    from flask import Flask
    
    error_app = Flask(__name__)
    
    @error_app.route('/')
    @error_app.route('/<path:path>')
    def error_handler(path=None):
        return json.dumps({
            'error': 'Application failed to load',
            'message': str(e),
            'type': type(e).__name__
        }), 500
    
    handler = error_app
