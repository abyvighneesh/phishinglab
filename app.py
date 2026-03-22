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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from utils.phishing_templates import get_phishing_templates, get_template_by_id
from utils.header_analysis import analyze_email_header
from utils.email_analysis import analyze_email
from utils.url_analysis import scan_url
from utils.login_page_detector import detect_fake_login
from utils.defense_engine import generate_defense_tips
from utils.models import db, User, Scan, QuizResult, PhishingTemplate, APILog, Achievement, Badge, Leaderboard
from utils.report_generator import generate_pdf_report, generate_csv_report
from utils.gamification_engine import (
    add_points_to_user, calculate_quiz_points, check_achievements,
    update_user_streak, get_user_stats, get_leaderboard,
    generate_daily_challenge, get_user_progress_stats
)
from utils.educational_engine import (
    create_default_modules, get_user_learning_progress,
    update_module_progress, get_learning_resources,
    generate_learning_recommendations
)
from utils.quiz_system import (
    get_quiz_by_module, get_puzzle_challenge, calculate_quiz_score,
    submit_quiz_attempt, get_user_quiz_stats
)
from utils.ip_geolocation import get_ip_geolocation, analyze_email_ips
from utils.phone_validator import analyze_phone_number, extract_phone_numbers, analyze_email_phones
from utils.qr_code_analyzer import analyze_qr_usage, get_qr_best_practices
from utils.image_analyzer import analyze_email_images
from utils.attachment_scanner import analyze_email_attachments, get_attachment_safety_checklist
from utils.auth_utils import (
    validate_password_strength, calculate_password_strength, 
    get_password_strength_label, generate_verification_token, 
    send_verification_email, is_verification_token_valid
)

# Get absolute path to static folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
DB_PATH = os.path.join(BASE_DIR, 'phishlab.db')

app = Flask(__name__, 
    static_folder=STATIC_FOLDER,
    static_url_path='/static')

# Security configuration - use environment variables in production
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'phishlab-educational-demo-2026-dev-only')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Production security settings
if os.getenv('FLASK_ENV') == 'production':
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create tables
with app.app_context():
    try:
        db.create_all()
        # Initialize default learning modules
        create_default_modules()
    except Exception as e:
        # Log database initialization errors but don't crash
        print(f"Warning: Database initialization error (this is okay on Vercel): {e}")
        pass

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
    """User registration with password strength validation"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Username and password required'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Validate password strength
        password_validation = validate_password_strength(password)
        if not password_validation['valid']:
            return jsonify({'error': password_validation['message']}), 400
        
        # Create user without email requirement
        user = User(
            username=username,
            email=f'{username}@phishlab.local',  # Auto-generated placeholder email
            password_hash=generate_password_hash(password),
            email_verified=True  # Auto-verified since we're not using email
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful! You can now login.',
            'redirect': url_for('login')
        }), 201
    
    return render_template('register.html')


@app.route('/verify-email/<token>')
def verify_email(token):
    """Verify user email with token"""
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        return render_template('verify_email.html', 
                             success=False, 
                             message='Invalid verification token')
    
    # Check if token has expired
    if not is_verification_token_valid(user.verification_token_created_at):
        return render_template('verify_email.html', 
                             success=False, 
                             message='Verification link has expired. Please register again.')
    
    # Mark email as verified
    user.email_verified = True
    user.verification_token = None
    user.verification_token_created_at = None
    db.session.commit()
    
    return render_template('verify_email.html', 
                         success=True, 
                         message='Email verified successfully! You can now log in.',
                         login_url=url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with email verification check"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check if email is verified
        if not user.email_verified:
            return jsonify({
                'error': 'Please verify your email before logging in. Check your inbox for the verification link.'
            }), 403
        
        login_user(user)
        return jsonify({'message': 'Login successful', 'redirect': url_for('dashboard')}), 200
    
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
@login_required
def simulate():
    """Display phishing email simulation page"""
    templates = get_phishing_templates()
    return render_template('simulate.html', templates=templates)


@app.route('/get-template/<int:template_id>')
@login_required
def get_template(template_id):
    """API endpoint to fetch a specific phishing template"""
    template = get_template_by_id(template_id)
    if template:
        return jsonify(template)
    return jsonify({'error': 'Template not found'}), 404


# ==================== EMAIL HEADER ANALYZER ====================

@app.route('/header-analyzer')
@login_required
def header_analyzer():
    """Display email header analyzer page"""
    return render_template('header_analyzer.html')


@app.route('/analyze-header', methods=['POST'])
@login_required
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
@login_required
def email_scanner():
    """Display email scanner page"""
    return render_template('email_scanner.html')


@app.route('/scan-email', methods=['POST'])
@login_required
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
@login_required
def url_scanner():
    """Display URL scanner page"""
    return render_template('url_scanner.html')


@app.route('/scan-url', methods=['POST'])
@login_required
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
@login_required
def login_detector():
    """Display fake login page detector"""
    return render_template('login_detector.html')


@app.route('/detect-login', methods=['POST'])
@login_required
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
@login_required
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


@app.route('/admin/api/add-user', methods=['POST'])
@admin_required
def admin_add_user():
    """Add a new user (admin endpoint)"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    password_validation = validate_password_strength(password)
    if not password_validation['valid']:
        return jsonify({'error': password_validation['message']}), 400
    
    user = User(
        username=username,
        email=f'{username}@phishlab.local',
        password_hash=generate_password_hash(password),
        email_verified=True
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201


@app.route('/admin/performance')
@admin_required
def admin_performance():
    """View logged-in student performance and activities"""
    users = User.query.filter_by(is_admin=False).all()
    
    performance_data = []
    for user in users:
        quizzes = QuizResult.query.filter_by(user_id=user.id).order_by(QuizResult.completed_at.desc()).all()
        scans = Scan.query.filter_by(user_id=user.id).order_by(Scan.created_at.desc()).all()
        
        if quizzes:
            avg_quiz_score = sum(q.score for q in quizzes) / len(quizzes)
        else:
            avg_quiz_score = 0
        
        # Get latest activity
        latest_activity_date = None
        activities = []
        
        # Collect quiz activities
        for quiz in quizzes[:5]:  # Last 5 quizzes
            activities.append({
                'type': '📝 Quiz',
                'description': f'Scored {quiz.percentage}%',
                'date': quiz.completed_at
            })
        
        # Collect scan activities
        for scan in scans[:5]:  # Last 5 scans
            scan_type_emoji = {
                'email': '📧',
                'url': '🔗',
                'header': '📋',
                'login': '🔐'
            }.get(scan.scan_type, '🔍')
            
            activities.append({
                'type': f'{scan_type_emoji} {scan.scan_type.title()}',
                'description': f'Risk: {scan.risk_score}%',
                'date': scan.created_at
            })
        
        activities.sort(key=lambda x: x['date'], reverse=True)
        if activities:
            latest_activity_date = activities[0]['date'].strftime('%Y-%m-%d %H:%M')
        else:
            latest_activity_date = 'No activity yet'
        
        performance_data.append({
            'user_id': user.id,
            'username': user.username,
            'total_points': user.total_points,
            'current_streak': user.current_streak,
            'skill_level': user.skill_level,
            'quizzes_completed': len(quizzes),
            'avg_quiz_score': round(avg_quiz_score, 2),
            'total_scans': len(scans),
            'joined_date': user.created_at.strftime('%Y-%m-%d'),
            'last_activity': latest_activity_date,
            'rank': user.rank,
            'activities': activities[:10]  # Last 10 activities
        })
    
    # Sort by latest activity date - alphabetical sort will put "No activity yet" at the end
    performance_data.sort(key=lambda x: x['last_activity'], reverse=True)
    
    return render_template('admin_performance.html', 
                         performance_data=performance_data,
                         total_students=len(performance_data))


# ==================== SETTINGS ===================="

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


# ==================== GAMIFICATION & ACHIEVEMENTS ====================

@app.route('/leaderboard')
@login_required
def leaderboard():
    """Display leaderboard"""
    top_users = get_leaderboard(limit=20)
    user_rank = None
    
    if current_user.is_authenticated:
        user_rank = next((u['rank'] for u in get_leaderboard(limit=1000) 
                         if u['username'] == current_user.username), None)
    
    return render_template('leaderboard.html', top_users=top_users, user_rank=user_rank)


@app.route('/api/stats')
@login_required
def get_stats():
    """Get user statistics and gamification data"""
    stats = get_user_stats(current_user.id)
    progress = get_user_progress_stats(current_user.id)
    challenge = generate_daily_challenge()
    
    return jsonify({
        'stats': stats,
        'progress': progress,
        'daily_challenge': challenge
    }), 200


@app.route('/api/achievements')
@login_required
def get_achievements():
    """Get user achievements and badges"""
    achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    badges = current_user.badges
    
    return jsonify({
        'achievements': [
            {
                'id': a.id,
                'title': a.title,
                'description': a.description,
                'points': a.points_earned,
                'type': a.achievement_type,
                'unlocked_at': a.unlocked_at.isoformat()
            }
            for a in achievements
        ],
        'badges': [
            {
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'icon': b.icon,
                'type': b.badge_type
            }
            for b in badges
        ]
    }), 200


# ==================== EDUCATIONAL CONTENT ====================

@app.route('/learning')
@login_required
def learning():
    """Display learning modules"""
    return render_template('learning.html')


@app.route('/api/learning-modules')
@login_required
def get_learning_modules():
    """Get all learning modules"""
    from utils.models import LearningModule
    modules = LearningModule.query.filter_by(is_published=True).all()
    
    user_progress = {}
    if current_user.is_authenticated:
        progress_data = get_user_learning_progress(current_user.id)
        if progress_data:
            user_progress = {m['id']: m for m in progress_data['modules']}
    
    return jsonify({
        'modules': [
            {
                'id': m.id,
                'title': m.title,
                'description': m.description,
                'category': m.category,
                'difficulty': m.difficulty,
                'duration': m.duration_minutes,
                'progress': user_progress.get(m.id, {}).get('progress', 0) if user_progress else 0,
                'completed': user_progress.get(m.id, {}).get('completed', False) if user_progress else False
            }
            for m in modules
        ]
    }), 200


@app.route('/api/learning-modules/<int:module_id>')
@login_required
def get_learning_module(module_id):
    """Get a specific learning module"""
    from utils.models import LearningModule
    module = LearningModule.query.get(module_id)
    
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    return jsonify({
        'id': module.id,
        'title': module.title,
        'description': module.description,
        'content': module.content,
        'category': module.category,
        'difficulty': module.difficulty,
        'duration': module.duration_minutes,
        'video_url': module.video_url
    }), 200


@app.route('/api/learning-progress', methods=['POST'])
@login_required
def update_learning_progress():
    """Update learning module progress"""
    data = request.get_json()
    module_id = data.get('module_id')
    progress = data.get('progress', 0)
    
    if not module_id:
        return jsonify({'error': 'Module ID required'}), 400
    
    update_module_progress(current_user.id, module_id, progress)
    
    # Add points if completed
    if progress >= 100:
        add_points_to_user(current_user.id, 30, 'learning_module')
        update_user_streak(current_user.id)
    
    return jsonify({'message': 'Progress updated'}), 200


@app.route('/api/learning-resources')
@login_required
def get_learning_resources_api():
    """Get learning resources"""
    category = request.args.get('category')
    resources = get_learning_resources(category)
    return jsonify({'resources': resources}), 200


@app.route('/api/learning-recommendations')
@login_required
def get_learning_recommendations_api():
    """Get personalized learning recommendations"""
    recommendations = generate_learning_recommendations(current_user.id)
    return jsonify({'recommendations': recommendations}), 200


# ==================== QUIZ & PUZZLE SYSTEM ====================

@app.route('/quiz')
@login_required
def quiz_page():
    """Display quiz page"""
    return render_template('quiz.html')


@app.route('/api/quiz/<int:module_id>')
@login_required
def get_module_quiz(module_id):
    """Get quiz questions for a specific module"""
    questions = get_quiz_by_module(module_id)
    return jsonify({'questions': questions}), 200


@app.route('/api/quiz/submit', methods=['POST'])
@login_required
def submit_quiz_api():
    """Submit quiz answers and calculate score"""
    data = request.get_json()
    module_id = data.get('module_id')
    answers = data.get('answers', {})
    
    # Calculate score
    score = calculate_quiz_score(current_user.id, answers)
    
    # Store attempt
    submit_quiz_attempt(current_user.id, module_id, answers, score)
    
    # Add points to user
    add_points_to_user(current_user.id, score['total_points'], 'quiz_completion')
    update_user_streak(current_user.id)
    check_achievements(current_user.id)
    
    # Build response with correct answer indicators
    questions = get_quiz_by_module(module_id)
    correct_by_question = {}
    for q in questions:
        correct_by_question[q['id']] = (answers.get(q['id']) == q['correct_answer'])
    
    return jsonify({
        'total_points': score['total_points'],
        'correct_answers': score['correct_answers'],
        'percentage': score['percentage'],
        'correct_by_question': correct_by_question
    }), 200


@app.route('/api/quiz/results')
@login_required
def get_quiz_results():
    """Get user's quiz statistics and results"""
    stats = get_user_quiz_stats(current_user.id)
    return jsonify({'stats': stats}), 200


@app.route('/api/puzzles')
@login_required
def get_puzzles():
    """Get all puzzle challenges"""
    from utils.quiz_system import PUZZLE_CHALLENGES
    
    puzzles = {}
    for key, challenge in PUZZLE_CHALLENGES.items():
        puzzles[key] = challenge
    
    return jsonify({'puzzles': puzzles}), 200


# ==================== ADDITIONAL DETECTION TOOLS ====================

@app.route('/ip-geolocation')
def ip_geolocation():
    """Display IP geolocation tool"""
    return render_template('ip_geolocation.html')


@app.route('/api/analyze-ip', methods=['POST'])
def analyze_ip():
    """Analyze IP address for geolocation and threats"""
    data = request.get_json()
    ip_address = data.get('ip', '')
    
    if not ip_address:
        return jsonify({'error': 'IP address required'}), 400
    
    result = get_ip_geolocation(ip_address)
    
    # Save to database
    if current_user.is_authenticated:
        from utils.models import DetectionResult
        detection = DetectionResult(
            user_id=current_user.id,
            detection_type='ip-geo',
            input_data=ip_address,
            result=result,
            risk_level=result.get('risk_level', 'unknown')
        )
        db.session.add(detection)
        db.session.commit()
        
        # Award points if threat found
        if result.get('risk_level') in ['high', 'critical']:
            add_points_to_user(current_user.id, 15, 'ip_scan')
    
    return jsonify(result), 200


@app.route('/phone-validator')
def phone_validator():
    """Display phone number validator tool"""
    return render_template('phone_validator.html')


@app.route('/api/analyze-phone', methods=['POST'])
def analyze_phone():
    """Analyze phone number for phishing indicators"""
    data = request.get_json()
    phone = data.get('phone', '')
    email_body = data.get('email_body', '')
    sender = data.get('sender', '')
    
    if not phone:
        return jsonify({'error': 'Phone number required'}), 400
    
    result = analyze_phone_number(phone, email_body, sender)
    
    # Save to database
    if current_user.is_authenticated:
        from utils.models import DetectionResult
        detection = DetectionResult(
            user_id=current_user.id,
            detection_type='phone',
            input_data=phone,
            result=result,
            risk_level=result.get('risk_level', 'unknown')
        )
        db.session.add(detection)
        db.session.commit()
        
        add_points_to_user(current_user.id, 15, 'phone_validation')
    
    return jsonify(result), 200


@app.route('/qr-analyzer')
def qr_analyzer():
    """Display QR code analyzer tool"""
    return render_template('qr_analyzer.html')


@app.route('/api/analyze-qr', methods=['POST'])
def analyze_qr():
    """Analyze QR code in email for phishing"""
    data = request.get_json()
    email_text = data.get('email_text', '')
    email_sender = data.get('sender', '')
    qr_url = data.get('qr_url', '')
    
    if not email_text:
        return jsonify({'error': 'Email text or QR URL required'}), 400
    
    result = analyze_qr_usage(email_text, email_sender, qr_url)
    best_practices = get_qr_best_practices()
    result['best_practices'] = best_practices
    
    # Save to database
    if current_user.is_authenticated:
        from utils.models import DetectionResult
        detection = DetectionResult(
            user_id=current_user.id,
            detection_type='qr',
            input_data=qr_url or email_text[:100],
            result=result,
            risk_level=result.get('risk_level', 'unknown')
        )
        db.session.add(detection)
        db.session.commit()
        
        add_points_to_user(current_user.id, 20, 'qr_analysis')
    
    return jsonify(result), 200


@app.route('/image-analyzer')
def image_analyzer():
    """Display image analyzer tool"""
    return render_template('image_analyzer.html')


@app.route('/api/analyze-images', methods=['POST'])
def analyze_images():
    """Analyze images in email for phishing"""
    data = request.get_json()
    html_content = data.get('html_content', '')
    email_context = data.get('email_context', '')
    
    if not html_content:
        return jsonify({'error': 'HTML content required'}), 400
    
    result = analyze_email_images(html_content, email_context)
    
    # Save to database
    if current_user.is_authenticated:
        from utils.models import DetectionResult
        detection = DetectionResult(
            user_id=current_user.id,
            detection_type='image',
            input_data='image-analysis',
            result=result,
            risk_level=result.get('risk_level', 'unknown')
        )
        db.session.add(detection)
        db.session.commit()
        
        add_points_to_user(current_user.id, 15, 'image_analysis')
    
    return jsonify(result), 200


@app.route('/attachment-scanner')
def attachment_scanner():
    """Display attachment scanner tool"""
    return render_template('attachment_scanner.html')


@app.route('/api/analyze-attachments', methods=['POST'])
def analyze_attachments():
    """Analyze email attachments for threats"""
    data = request.get_json()
    attachments = data.get('attachments', [])
    email_subject = data.get('subject', '')
    email_body = data.get('body', '')
    
    if not attachments:
        return jsonify({'error': 'Attachments required'}), 400
    
    result = analyze_email_attachments(attachments, email_subject, email_body)
    safety_checklist = get_attachment_safety_checklist()
    result['safety_checklist'] = safety_checklist
    
    # Save to database
    if current_user.is_authenticated:
        from utils.models import DetectionResult
        detection = DetectionResult(
            user_id=current_user.id,
            detection_type='attachment',
            input_data=str([a.get('filename') for a in attachments])[:100],
            result=result,
            risk_level=result.get('overall_risk_level', 'unknown')
        )
        db.session.add(detection)
        db.session.commit()
        
        add_points_to_user(current_user.id, 25, 'attachment_scan')
    
    return jsonify(result), 200


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
    
    # Development mode only
    debug_mode = os.getenv('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

