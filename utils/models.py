"""
PhishLab Database Models
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User account model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=True)  # Optional for testing
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Email verification fields
    email_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(255), nullable=True)
    verification_token_created_at = db.Column(db.DateTime, nullable=True)
    
    # Gamification fields
    total_points = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_activity = db.Column(db.DateTime)
    skill_level = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced, Expert
    
    # Relationships
    scans = db.relationship('Scan', backref='user', lazy=True, cascade='all, delete-orphan')
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('Achievement', backref='user', lazy=True, cascade='all, delete-orphan')
    badges = db.relationship('Badge', secondary='user_badges', backref=db.backref('users', lazy=True))
    learning_progress = db.relationship('LearningProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    
    @property
    def rank(self):
        """Calculate user rank based on total points"""
        if self.total_points >= 5000:
            return 'Security Master'
        elif self.total_points >= 3000:
            return 'Phishing Expert'
        elif self.total_points >= 1500:
            return 'Advanced Guardian'
        elif self.total_points >= 500:
            return 'Skilled Defender'
        else:
            return 'Security Learner'
    
    def __repr__(self):
        return f'<User {self.username}>'


class Scan(db.Model):
    """Track user scans and analyses"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False)  # 'url', 'header', 'login', etc.
    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.JSON, nullable=False)
    risk_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Scan {self.scan_type} - {self.created_at}>'


class QuizResult(db.Model):
    """Track quiz performance"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    answers = db.Column(db.JSON, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def percentage(self):
        """Calculate percentage score"""
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 2)
    
    def __repr__(self):
        return f'<QuizResult {self.percentage}% - {self.completed_at}>'


class PhishingTemplate(db.Model):
    """Manage phishing templates"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    email_content = db.Column(db.Text, nullable=False)
    red_flags = db.Column(db.JSON, nullable=False)
    attack_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PhishingTemplate {self.name}>'


class APILog(db.Model):
    """Log API usage"""
    id = db.Column(db.Integer, primary_key=True)
    endpoint = db.Column(db.String(200), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    status_code = db.Column(db.Integer)
    response_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<APILog {self.endpoint} {self.method}>'


# ==================== GAMIFICATION MODELS ====================

class Achievement(db.Model):
    """Track user achievements and milestones"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    points_earned = db.Column(db.Integer, default=100)
    achievement_type = db.Column(db.String(50), nullable=False)  # 'quiz', 'scan', 'streak', 'milestone'
    achievement_data = db.Column(db.JSON)  # Additional metadata
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Achievement {self.title}>'


class Badge(db.Model):
    """Badge template"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(200))  # Icon filename or emoji
    requirement = db.Column(db.String(255))  # How to earn the badge
    badge_type = db.Column(db.String(50))  # 'phishing-expert', 'speed-demon', 'perfect-score', etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Badge {self.name}>'


user_badges = db.Table('user_badges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('badge_id', db.Integer, db.ForeignKey('badge.id'), primary_key=True),
    db.Column('earned_at', db.DateTime, default=datetime.utcnow)
)


class Leaderboard(db.Model):
    """Leaderboard entries"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rank = db.Column(db.Integer)
    points = db.Column(db.Integer, nullable=False)
    quizzes_completed = db.Column(db.Integer, default=0)
    perfect_scans = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Leaderboard Rank {self.rank}>'


# ==================== EDUCATIONAL MODELS ====================

class LearningModule(db.Model):
    """Educational learning modules"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)  # HTML content
    category = db.Column(db.String(100), nullable=False)  # 'email-phishing', 'url-analysis', 'social-engineering', etc.
    difficulty = db.Column(db.String(20), default='Intermediate')  # Beginner, Intermediate, Advanced
    duration_minutes = db.Column(db.Integer, default=15)
    video_url = db.Column(db.String(500))  # Optional video link
    quiz_id = db.Column(db.Integer)  # Reference to associated quiz
    created_by = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<LearningModule {self.title}>'


class LearningResource(db.Model):
    """External learning resources"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    resource_type = db.Column(db.String(50))  # 'article', 'video', 'guide', 'tool'
    category = db.Column(db.String(100))
    source = db.Column(db.String(120))
    is_external = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningResource {self.title}>'


class LearningProgress(db.Model):
    """Track user progress on learning modules"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('learning_module.id'), nullable=False)
    progress_percentage = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LearningProgress {self.progress_percentage}%>'


class CertificationQuiz(db.Model):
    """Certification quiz questions and answers"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    passing_score = db.Column(db.Integer, default=70)
    total_questions = db.Column(db.Integer, default=10)
    questions = db.Column(db.JSON, nullable=False)  # List of question objects
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<CertificationQuiz {self.title}>'


class CertificationResult(db.Model):
    """Track certification quiz results"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('certification_quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_token = db.Column(db.String(255))  # Unique token for verification
    
    def __repr__(self):
        return f'<CertificationResult {self.score}/100>'


# ==================== DETECTION MODELS ====================

class DetectionResult(db.Model):
    """Track results from detection tools"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    detection_type = db.Column(db.String(50), nullable=False)  # 'ip-geo', 'phone', 'qr', 'image', 'attachment'
    input_data = db.Column(db.Text, nullable=False)
    result = db.Column(db.JSON, nullable=False)
    risk_level = db.Column(db.String(20))  # 'low', 'medium', 'high', 'critical'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DetectionResult {self.detection_type}>'


class IPGeolocation(db.Model):
    """Cache IP geolocation lookups"""
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50), unique=True, nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    isp = db.Column(db.String(255))
    threat_level = db.Column(db.String(20))  # 'safe', 'suspicious', 'malicious'
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<IPGeolocation {self.ip_address}>'
