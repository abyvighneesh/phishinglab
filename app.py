"""
PhishLab: End-to-End Phishing Simulation & Defense Framework

ETHICAL DISCLAIMER:
This project is strictly for educational and awareness purposes only.
It does not perform real phishing attacks, credential harvesting, or malicious activity.
All simulations are safe and offline.

Author: Cybersecurity Education Team
Date: 2026
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from utils.phishing_templates import get_phishing_templates, get_template_by_id
from utils.header_analysis import analyze_email_header
from utils.url_analysis import scan_url
from utils.login_page_detector import detect_fake_login
from utils.defense_engine import generate_defense_tips

# Get absolute path to static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, 
    static_folder=STATIC_FOLDER,
    static_url_path='/static')
app.config['SECRET_KEY'] = 'phishlab-educational-demo-2026'

# Home route
@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')

# Phishing simulation module
@app.route('/simulate')
def simulate():
    """Display phishing email simulation page"""
    templates = get_phishing_templates()
    return render_template('simulate.html', templates=templates)

@app.route('/get-template/<int:template_id>')
def get_template(template_id):
    """API endpoint to fetch a specific phishing template"""
    template = get_template_by_id(template_id)
    if template:
        return jsonify(template)
    return jsonify({'error': 'Template not found'}), 404

# Email header analyzer module
@app.route('/header-analyzer')
def header_analyzer():
    """Display email header analyzer page"""
    return render_template('header_analyzer.html')

@app.route('/analyze-header', methods=['POST'])
def analyze_header():
    """Analyze email headers for phishing indicators"""
    data = request.get_json()
    header_text = data.get('header', '')
    
    if not header_text:
        return jsonify({'error': 'No header provided'}), 400
    
    # Perform analysis
    analysis_result = analyze_email_header(header_text)
    
    # Generate defense recommendations
    defense_tips = generate_defense_tips(
        analysis_result['risk_score'],
        analysis_result['indicators']
    )
    analysis_result['defense_recommendations'] = defense_tips
    
    return jsonify(analysis_result)

# URL scanner module
@app.route('/url-scanner')
def url_scanner():
    """Display URL scanner page"""
    return render_template('url_scanner.html')

@app.route('/scan-url', methods=['POST'])
def scan_url_route():
    """Scan URL for phishing indicators"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Perform URL analysis
    scan_result = scan_url(url)
    
    # Generate defense recommendations
    defense_tips = generate_defense_tips(
        scan_result['risk_score'],
        scan_result['indicators']
    )
    scan_result['defense_recommendations'] = defense_tips
    
    return jsonify(scan_result)

# Fake login page detector module
@app.route('/login-detector')
def login_detector():
    """Display fake login page detector"""
    return render_template('login_detector.html')

@app.route('/detect-login', methods=['POST'])
def detect_login_route():
    """Detect fake login pages"""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Perform login page detection
    detection_result = detect_fake_login(url)
    
    # Generate defense recommendations
    defense_tips = generate_defense_tips(
        detection_result['risk_score'],
        detection_result['indicators']
    )
    detection_result['defense_recommendations'] = defense_tips
    
    return jsonify(detection_result)

# Awareness module
@app.route('/awareness')
def awareness():
    """Display phishing awareness and education dashboard"""
    return render_template('awareness.html')

# Result page (generic)
@app.route('/result')
def result():
    """Display analysis results"""
    return render_template('result.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("PhishLab: Ethical Phishing Simulation Framework")
    print("=" * 60)
    print("\nETHICAL DISCLAIMER:")
    print("This is an EDUCATIONAL tool for cybersecurity awareness.")
    print("No real phishing attacks are performed.")
    print("All simulations are safe and offline.\n")
    print("=" * 60)
    print(f"Static files served from: {STATIC_FOLDER}")
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

