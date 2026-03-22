"""
Vercel serverless entry point for PhishLab Flask app
"""
import sys
import os

# Set production environment
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Add parent directory to path
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

try:
    from app import app
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error_response():
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
