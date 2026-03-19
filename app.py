"""
PhishLab: End-to-End Phishing Simulation & Defense Framework

ETHICAL DISCLAIMER:
This project is strictly for educational and awareness purposes only.
It does not perform real phishing attacks, credential harvesting, or malicious activity.
All simulations are safe and offline.

Author: Cybersecurity Education Team
Date: 2026
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import datetime
from functools import wraps

from utils.phishing_templates import get_phishing_templates, get_template_by_id
from utils.header_analysis import analyze_email_header
from utils.email_analysis import analyze_email
from utils.url_analysis import scan_url
from utils.login_page_detector import detect_fake_login
from utils.defense_engine import generate_defense_tips
from utils.models import db, User, Scan, QuizResult, PhishingTemplate, APILog
from utils.report_generator import generate_pdf_report, generate_csv_report

# Get absolute path to static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
DB_PATH = os.path.join(BASE_DIR, 'phishlab.db')

app = Flask(__name__, 
    static_folder=STATIC_FOLDER,
    static_url_path='/static')
app.config['SECRET_KEY'] = 'phishlab-educational-demo-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper function for admin check
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Helper function to log API calls
def log_api_call(endpoint, method, status_code, response_time=0):
    log = APILog(endpoint=endpoint, method=method, status_code=status_code, response_time=response_time)
    db.session.add(log)
    db.session.commit()

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'All fields required'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful', 'redirect': url_for('login')}), 201
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return jsonify({'message': 'Login successful', 'redirect': url_for('dashboard')}), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    return redirect(url_for('index'))


# ==================== MAIN ROUTES ====================

@app.route('/')
def index():
    """Main landing page"""
    return render_template('index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with statistics"""
    user_scans = Scan.query.filter_by(user_id=current_user.id).all()
    quiz_results = QuizResult.query.filter_by(user_id=current_user.id).all()
    
    stats = {
        'total_scans': len(user_scans),
        'total_quizzes': len(quiz_results),
        'avg_risk_score': round(sum(s.risk_score for s in user_scans) / len(user_scans), 2) if user_scans else 0,
        'avg_quiz_score': round(sum(q.percentage for q in quiz_results) / len(quiz_results), 2) if quiz_results else 0
    }
    
    return render_template('dashboard.html', stats=stats, scans=user_scans, quiz_results=quiz_results)

# ==================== PHISHING SIMULATION ====================

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


# ==================== EMAIL HEADER ANALYZER ====================

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
    
    # Save to database if user is logged in
    if current_user.is_authenticated:
        scan = Scan(
            user_id=current_user.id,
            scan_type='header',
            input_data=header_text[:100],
            result=analysis_result,
            risk_score=analysis_result['risk_score']
        )
        db.session.add(scan)
        db.session.commit()
    
    return jsonify(analysis_result)


# ==================== EMAIL SCANNER ====================

@app.route('/email-scanner')
def email_scanner():
    """Display email scanner page"""
    return render_template('email_scanner.html')


@app.route('/scan-email', methods=['POST'])
def scan_email_route():
    """Scan full email for phishing indicators"""
    data = request.get_json()
    email_content = data.get('email', '')
    
    if not email_content:
        return jsonify({'error': 'No email content provided'}), 400
    
    # Perform email analysis
    scan_result = analyze_email(email_content)
    
    # Generate defense recommendations
    defense_tips = generate_defense_tips(
        scan_result['risk_score'],
        scan_result['indicators']
    )
    scan_result['defense_recommendations'] = defense_tips
    
    # Save to database if user is logged in
    if current_user.is_authenticated:
        scan = Scan(
            user_id=current_user.id,
            scan_type='email',
            input_data=email_content[:100],
            result=scan_result,
            risk_score=scan_result['risk_score']
        )
        db.session.add(scan)
        db.session.commit()
    
    return jsonify(scan_result)


# ==================== URL SCANNER ====================

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
    
    # Save to database if user is logged in
    if current_user.is_authenticated:
        scan = Scan(
            user_id=current_user.id,
            scan_type='url',
            input_data=url,
            result=scan_result,
            risk_score=scan_result['risk_score']
        )
        db.session.add(scan)
        db.session.commit()
    
    return jsonify(scan_result)


# ==================== LOGIN DETECTOR ====================

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
    
    # Save to database if user is logged in
    if current_user.is_authenticated:
        scan = Scan(
            user_id=current_user.id,
            scan_type='login',
            input_data=url,
            result=detection_result,
            risk_score=detection_result['risk_score']
        )
        db.session.add(scan)
        db.session.commit()
    
    return jsonify(detection_result)


# ==================== AWARENESS ====================

@app.route('/awareness')
def awareness():
    """Display phishing awareness and education dashboard"""
    return render_template('awareness.html')


@app.route('/submit-quiz', methods=['POST'])
@login_required
def submit_quiz():
    """Submit quiz answers"""
    data = request.get_json()
    answers = data.get('answers', {})
    
    # Simple scoring: correct answers
    correct_answers = {'q1': 'b', 'q2': 'a', 'q3': 'c'}
    score = sum(1 for q, ans in answers.items() if correct_answers.get(q) == ans)
    
    quiz_result = QuizResult(
        user_id=current_user.id,
        score=score,
        total_questions=len(correct_answers),
        answers=answers
    )
    db.session.add(quiz_result)
    db.session.commit()
    
    return jsonify({
        'score': score,
        'percentage': quiz_result.percentage,
        'message': f'Quiz completed! Your score: {quiz_result.percentage}%'
    })


# ==================== EXPORT FUNCTIONALITY ====================

@app.route('/export/pdf/<int:scan_id>')
@login_required
def export_pdf(scan_id):
    """Export scan as PDF"""
    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
    
    pdf_buffer = generate_pdf_report(
        scan.scan_type,
        scan.input_data,
        scan.result,
        scan.risk_score,
        current_user
    )
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'phishlab_report_{scan.id}.pdf'
    )


@app.route('/export/csv')
@login_required
def export_csv():
    """Export all scans as CSV"""
    scans = Scan.query.filter_by(user_id=current_user.id).all()
    csv_buffer = generate_csv_report(scans)
    
    return send_file(
        csv_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'phishlab_scans_{datetime.now().strftime("%Y%m%d")}.csv'
    )


# ==================== API ENDPOINTS ====================

@app.route('/api/v1/scan/url', methods=['POST'])
def api_scan_url():
    """API endpoint for URL scanning"""
    data = request.get_json()
    url = data.get('url', '')
    api_key = request.headers.get('X-API-Key')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    result = scan_url(url)
    result['defense_recommendations'] = generate_defense_tips(result['risk_score'], result['indicators'])
    
    log_api_call('/api/v1/scan/url', 'POST', 200)
    
    return jsonify(result), 200


@app.route('/api/v1/scan/header', methods=['POST'])
def api_scan_header():
    """API endpoint for header scanning"""
    data = request.get_json()
    header = data.get('header', '')
    
    if not header:
        return jsonify({'error': 'No header provided'}), 400
    
    result = analyze_email_header(header)
    result['defense_recommendations'] = generate_defense_tips(result['risk_score'], result['indicators'])
    
    log_api_call('/api/v1/scan/header', 'POST', 200)
    
    return jsonify(result), 200


@app.route('/api/v1/history', methods=['GET'])
@login_required
def api_get_history():
    """API endpoint to get scan history"""
    scans = Scan.query.filter_by(user_id=current_user.id).all()
    
    history = [{
        'id': scan.id,
        'type': scan.scan_type,
        'input': scan.input_data,
        'risk_score': scan.risk_score,
        'date': scan.created_at.isoformat()
    } for scan in scans]
    
    log_api_call('/api/v1/history', 'GET', 200)
    return jsonify(history), 200


# ==================== ADMIN PANEL ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    total_users = User.query.count()
    total_scans = Scan.query.count()
    total_quizzes = QuizResult.query.count()
    api_logs = APILog.query.order_by(APILog.created_at.desc()).limit(10).all()
    
    stats = {
        'total_users': total_users,
        'total_scans': total_scans,
        'total_quizzes': total_quizzes,
        'api_logs': api_logs
    }
    
    return render_template('admin.html', stats=stats)


@app.route('/admin/users')
@admin_required
def admin_users():
    """Manage users"""
    users = User.query.all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/templates')
@admin_required
def admin_templates():
    """Manage phishing templates"""
    templates = PhishingTemplate.query.all()
    return render_template('admin_templates.html', templates=templates)


@app.route('/admin/api/add-template', methods=['POST'])
@admin_required
def admin_add_template():
    """Add new phishing template"""
    data = request.get_json()
    
    template = PhishingTemplate(
        name=data.get('name'),
        description=data.get('description'),
        email_content=data.get('email_content'),
        red_flags=data.get('red_flags', []),
        attack_type=data.get('attack_type')
    )
    db.session.add(template)
    db.session.commit()
    
    return jsonify({'message': 'Template added', 'id': template.id}), 201


@app.route('/admin/api/delete-user/<int:user_id>', methods=['DELETE'])
@admin_required
def admin_delete_user(user_id):
    """Delete user and their data"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404


# ==================== SETTINGS ====================

@app.route('/settings')
@login_required
def settings():
    """User settings"""
    return render_template('settings.html', user=current_user)


@app.route('/api/settings/theme', methods=['POST'])
@login_required
def set_theme():
    """Set user theme preference"""
    data = request.get_json()
    theme = data.get('theme', 'light')
    session['theme'] = theme
    return jsonify({'message': 'Theme updated', 'theme': theme}), 200


# ==================== RESULT PAGE ====================

@app.route('/result')
def result():
    """Display analysis results"""
    return render_template('result.html')


# ==================== ERROR HANDLERS ====================

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
    print(f"Database: {DB_PATH}")
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press CTRL+C to quit\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

