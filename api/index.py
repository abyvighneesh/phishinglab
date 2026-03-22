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

# Import the Flask app from app.py
from app import app

# Export the app for Vercel
# Vercel will call this as a WSGI application
handler = app
