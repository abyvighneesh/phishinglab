"""
Authentication Utilities
Password strength validation and email verification
"""

import re
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Password strength requirements
PASSWORD_REQUIREMENTS = {
    'min_length': 8,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special': True,
}

SPECIAL_CHARS = r'!@#$%^&*()_+-=[]{}|;:,.<>?'


def validate_password_strength(password):
    """
    Validate password meets all strength requirements
    Returns: (is_valid: bool, requirements: dict}
    """
    requirements = {
        'length': len(password) >= PASSWORD_REQUIREMENTS['min_length'],
        'uppercase': bool(re.search(r'[A-Z]', password)) if PASSWORD_REQUIREMENTS['require_uppercase'] else True,
        'lowercase': bool(re.search(r'[a-z]', password)) if PASSWORD_REQUIREMENTS['require_lowercase'] else True,
        'numbers': bool(re.search(r'\d', password)) if PASSWORD_REQUIREMENTS['require_numbers'] else True,
        'special': bool(re.search(f'[{re.escape(SPECIAL_CHARS)}]', password)) if PASSWORD_REQUIREMENTS['require_special'] else True,
    }
    
    all_valid = all(requirements.values())
    
    return {
        'valid': all_valid,
        'requirements': requirements,
        'message': get_password_feedback(requirements, password)
    }


def get_password_feedback(requirements, password):
    """Generate user-friendly password feedback"""
    if all(requirements.values()):
        return 'Strong password ✓'
    
    missing = []
    if not requirements['length']:
        missing.append(f'at least {PASSWORD_REQUIREMENTS["min_length"]} characters')
    if not requirements['uppercase']:
        missing.append('uppercase letter (A-Z)')
    if not requirements['lowercase']:
        missing.append('lowercase letter (a-z)')
    if not requirements['numbers']:
        missing.append('number (0-9)')
    if not requirements['special']:
        missing.append(f'special character ({SPECIAL_CHARS})')
    
    return 'Password needs: ' + ', '.join(missing)


def calculate_password_strength(password):
    """Calculate password strength score 0-100"""
    score = 0
    
    # Length scoring
    if len(password) >= 8:
        score += 10
    if len(password) >= 12:
        score += 10
    if len(password) >= 16:
        score += 10
    
    # Character variety
    if re.search(r'[a-z]', password):
        score += 15
    if re.search(r'[A-Z]', password):
        score += 15
    if re.search(r'\d', password):
        score += 15
    if re.search(f'[{re.escape(SPECIAL_CHARS)}]', password):
        score += 20
    
    # Bonus for mixing
    if re.search(r'[a-z].*[A-Z]|[A-Z].*[a-z]', password):
        score += 5
    
    return min(score, 100)


def get_password_strength_label(score):
    """Get strength label based on score"""
    if score >= 80:
        return 'Very Strong'
    elif score >= 60:
        return 'Strong'
    elif score >= 40:
        return 'Fair'
    elif score >= 20:
        return 'Weak'
    else:
        return 'Very Weak'


def generate_verification_token():
    """Generate a secure verification token"""
    return secrets.token_urlsafe(32)


def send_verification_email(user_email, username, verification_token, verification_link):
    """
    Send email verification link
    
    Note: This requires email configuration. For development, you can skip SMTP setup.
    In production, configure SMTP settings.
    """
    try:
        # For development/demo: just return True
        # In production, implement SMTP:
        """
        sender_email = os.getenv('SMTP_EMAIL', 'noreply@phishlab.local')
        sender_password = os.getenv('SMTP_PASSWORD', '')
        smtp_server = os.getenv('SMTP_SERVER', 'localhost')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Verify your PhishLab Email'
        message['From'] = sender_email
        message['To'] = user_email
        
        text = f"""
        Hi {username},
        
        Welcome to PhishLab! Please verify your email address by clicking the link below:
        
        {verification_link}
        
        This link will expire in 24 hours.
        
        If you did not create this account, please ignore this email.
        
        Best regards,
        PhishLab Team
        """
        
        html = f"""
        <html>
            <body>
                <h2>Welcome to PhishLab!</h2>
                <p>Hi {username},</p>
                <p>Please verify your email address by clicking the button below:</p>
                <p><a href="{verification_link}" style="background-color:#007bff;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">Verify Email</a></p>
                <p>Or copy this link: {verification_link}</p>
                <p><small>This link will expire in 24 hours.</small></p>
                <p>If you did not create this account, please ignore this email.</p>
                <p>Best regards,<br/>PhishLab Team</p>
            </body>
        </html>
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        message.attach(part1)
        message.attach(part2)
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, user_email, message.as_string())
        server.quit()
        """
        
        # Development mode: just log it
        print(f"\n📧 [EMAIL WOULD BE SENT]")
        print(f"To: {user_email}")
        print(f"Subject: Verify your PhishLab Email")
        print(f"Verification Link: {verification_link}\n")
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def is_verification_token_valid(token_created_at):
    """Check if verification token is still valid (24 hours)"""
    if not token_created_at:
        return False
    
    expiry_time = token_created_at + timedelta(hours=24)
    return datetime.utcnow() < expiry_time
