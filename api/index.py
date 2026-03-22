"""
Vercel serverless entry point for PhishLab Flask app
Vercel's Python builder looks for a WSGI-compatible app in /api
"""
import sys
import os

# Set production environment BEFORE importing Flask app
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Add parent directory to path so we can import the main app
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    # Import and initialize Flask app from parent directory
    from app import app as flask_app
    
    # This is what Vercel will use as the WSGI application
    app = flask_app
    
except Exception as e:
    # Fallback - if main app import fails, provide a debug endpoint
    print(f"ERROR importing Flask app: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def debug():
        return jsonify({
            'status': 'error',
            'message': 'Failed to load PhishLab Flask application',
            'error_type': type(e).__name__,
            'error_details': str(e)
        }), 500
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'status': 'error', 'message': 'Not Found'}), 404

