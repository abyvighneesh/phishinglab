"""
Gamification Engine
Manages points, badges, achievements, leaderboards, and user progression
"""

from datetime import datetime, timedelta
from utils.models import db, User, Achievement, Badge, Leaderboard

# Points earned for various activities
POINTS_CONFIG = {
    'quiz_completion': 50,
    'quiz_perfect': 100,
    'quiz_per_10_percent': 10,  # 10 points for every 10% score
    'url_scan': 20,
    'url_scan_threat_found': 50,
    'header_scan': 20,
    'header_scan_threat_found': 50,
    'login_detection': 20,
    'login_detection_threat_found': 50,
    'ip_scan': 15,
    'phone_validation': 15,
    'qr_analysis': 20,
    'image_analysis': 15,
    'attachment_scan': 25,
    'learning_module': 30,
    'learning_module_quiz': 40,
    'certification': 200,
    'certification_passed': 300,
    'streak_5_days': 100,
    'streak_30_days': 500,
}

# Badge definitions
BADGE_DEFINITIONS = {
    'first_scan': {
        'name': 'First Step',
        'description': 'Complete your first phishing scan',
        'icon': '👣',
        'points': 25
    },
    'threat_hunter': {
        'name': 'Threat Hunter',
        'description': 'Identify 10 phishing threats',
        'icon': '🔍',
        'points': 100,
        'requirement': 'threats_found >= 10'
    },
    'quiz_master': {
        'name': 'Quiz Master',
        'description': 'Complete 5 quizzes with 90%+ score',
        'icon': '🎓',
        'points': 150,
        'requirement': 'perfect_quizzes >= 5'
    },
    'perfect_score': {
        'name': 'Perfect Score',
        'description': 'Get 100% on a quiz',
        'icon': '💯',
        'points': 75,
        'requirement': 'quiz_score == 100'
    },
    'speed_demon': {
        'name': 'Speed Demon',
        'description': 'Complete 3 scans in under 2 minutes each',
        'icon': '⚡',
        'points': 100,
        'requirement': 'fast_scans >= 3'
    },
    'consistent_defender': {
        'name': 'Consistent Defender',
        'description': 'Maintain a 7-day activity streak',
        'icon': '🏆',
        'points': 150,
        'requirement': 'streak >= 7'
    },
    'security_expert': {
        'name': 'Security Expert',
        'description': 'Complete all learning modules',
        'icon': '🔐',
        'points': 300,
        'requirement': 'modules_completed >= 8'
    },
    'certified_defender': {
        'name': 'Certified Defender',
        'description': 'Pass a certification quiz',
        'icon': '🎖️',
        'points': 250,
        'requirement': 'certification_passed'
    },
    'multi_tool_master': {
        'name': 'Multi-Tool Master',
        'description': 'Use all detection tools',
        'icon': '🛠️',
        'points': 120,
        'requirement': 'tools_used >= 8'
    },
    'leaderboard_champion': {
        'name': 'Leaderboard Champion',
        'description': 'Reach top position on leaderboard',
        'icon': '👑',
        'points': 500,
        'requirement': 'rank == 1'
    },
}

# Skill levels and progression
SKILL_LEVELS = {
    'Beginner': {'min_points': 0, 'description': 'Just starting your security journey'},
    'Novice': {'min_points': 100, 'description': 'Learning the basics'},
    'Intermediate': {'min_points': 500, 'description': 'Growing your skills'},
    'Advanced': {'min_points': 1500, 'description': 'Strong security knowledge'},
    'Expert': {'min_points': 3000, 'description': 'Mastering phishing detection'},
    'Master': {'min_points': 5000, 'description': 'Security expert level'},
}


def add_points_to_user(user_id, points, activity_type=''):
    """Add points to user account"""
    user = User.query.get(user_id)
    if not user:
        return False
    
    user.total_points += points
    user.last_activity = datetime.utcnow()
    
    db.session.commit()
    
    return {
        'user_id': user_id,
        'points_added': points,
        'total_points': user.total_points,
        'activity': activity_type
    }


def calculate_quiz_points(score, total_questions):
    """Calculate points earned from quiz"""
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    points = int((percentage / 100) * POINTS_CONFIG['quiz_completion'])
    
    if percentage == 100:
        points += POINTS_CONFIG['quiz_perfect']
    
    return points


def calculate_scan_points(scan_type, threat_found):
    """Calculate points for a scan"""
    base_points = POINTS_CONFIG.get(f'{scan_type}_scan', 20)
    
    if threat_found:
        base_points += POINTS_CONFIG.get(f'{scan_type}_scan_threat_found', 30)
    
    return base_points


def check_achievements(user_id):
    """Check and award achievements for user"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    new_achievements = []
    
    # Check first scan
    if user.scans and not Achievement.query.filter_by(
        user_id=user_id, title='First Step'
    ).first():
        achievement = Achievement(
            user_id=user_id,
            title='First Step',
            description='Complete your first phishing scan',
            points_earned=25,
            achievement_type='scan'
        )
        db.session.add(achievement)
        new_achievements.append('First Step')
    
    # Check threat hunter (10 threats found)
    threats_found = sum(1 for s in user.scans if s.risk_score > 50)
    if threats_found >= 10 and not Achievement.query.filter_by(
        user_id=user_id, title='Threat Hunter'
    ).first():
        achievement = Achievement(
            user_id=user_id,
            title='Threat Hunter',
            description='Identify 10 phishing threats',
            points_earned=100,
            achievement_type='milestone'
        )
        db.session.add(achievement)
        new_achievements.append('Threat Hunter')
    
    # Check perfect quizzes (5 quizzes with 90%+)
    perfect_quizzes = sum(1 for q in user.quiz_results if q.percentage >= 90)
    if perfect_quizzes >= 5 and not Achievement.query.filter_by(
        user_id=user_id, title='Quiz Master'
    ).first():
        achievement = Achievement(
            user_id=user_id,
            title='Quiz Master',
            description='Complete 5 quizzes with 90%+ score',
            points_earned=150,
            achievement_type='quiz'
        )
        db.session.add(achievement)
        new_achievements.append('Quiz Master')
    
    db.session.commit()
    return new_achievements


def check_badge_unlocks(user_id):
    """Check for badge unlocks"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    new_badges = []
    
    # Get or create badgesfrom BADGE_DEFINITIONS
    for badge_key, badge_info in BADGE_DEFINITIONS.items():
        badge = Badge.query.filter_by(name=badge_info['name']).first()
        if not badge:
            badge = Badge(
                name=badge_info['name'],
                description=badge_info['description'],
                icon=badge_info['icon'],
                badge_type=badge_key
            )
            db.session.add(badge)
    
    db.session.commit()
    
    return new_badges


def update_user_streak(user_id):
    """Update user activity streak"""
    user = User.query.get(user_id)
    if not user:
        return
    
    today = datetime.utcnow().date()
    last_activity = user.last_activity
    
    if last_activity:
        last_activity_date = last_activity.date()
        days_since = (today - last_activity_date).days
        
        if days_since == 0:
            # Same day, streak continues
            pass
        elif days_since == 1:
            # Consecutive day, increment streak
            user.current_streak += 1
            if user.current_streak > user.longest_streak:
                user.longest_streak = user.current_streak
        else:
            # Streak broken
            user.current_streak = 1
    else:
        # First activity
        user.current_streak = 1
    
    user.last_activity = datetime.utcnow()
    db.session.commit()
    
    return user.current_streak


def get_user_stats(user_id):
    """Get comprehensive user statistics"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    stats = {
        'username': user.username,
        'total_points': user.total_points,
        'skill_level': user.skill_level,
        'rank': user.rank,
        'current_streak': user.current_streak,
        'longest_streak': user.longest_streak,
        'total_scans': len(user.scans),
        'total_quizzes': len(user.quiz_results),
        'avg_quiz_score': 0,
        'achievements': len(user.achievements),
        'badges': len(user.badges),
        'threats_detected': 0,
        'perfect_scans': 0,
    }
    
    if user.quiz_results:
        stats['avg_quiz_score'] = round(
            sum(q.percentage for q in user.quiz_results) / len(user.quiz_results), 2
        )
    
    stats['threats_detected'] = sum(1 for s in user.scans if s.risk_score > 50)
    stats['perfect_scans'] = sum(1 for s in user.scans if s.risk_score >= 80)
    
    return stats


def update_leaderboard():
    """Update leaderboard rankings"""
    users = User.query.all()
    
    # Sort by total points descending
    ranked_users = sorted(users, key=lambda u: u.total_points, reverse=True)
    
    for rank, user in enumerate(ranked_users, 1):
        leaderboard = Leaderboard.query.filter_by(user_id=user.id).first()
        
        if not leaderboard:
            leaderboard = Leaderboard(user_id=user.id)
            db.session.add(leaderboard)
        
        leaderboard.rank = rank
        leaderboard.points = user.total_points
        leaderboard.quizzes_completed = len(user.quiz_results)
        leaderboard.perfect_scans = sum(1 for s in user.scans if s.risk_score >= 80)
        leaderboard.updated_at = datetime.utcnow()
    
    db.session.commit()


def get_leaderboard(limit=10):
    """Get top users from leaderboard"""
    update_leaderboard()
    
    leaderboards = Leaderboard.query.order_by(
        Leaderboard.rank
    ).limit(limit).all()
    
    result = []
    for lb in leaderboards:
        user = User.query.get(lb.user_id)
        result.append({
            'rank': lb.rank,
            'username': user.username,
            'points': lb.points,
            'skill_level': user.skill_level,
            'quizzes_completed': lb.quizzes_completed,
            'perfect_scans': lb.perfect_scans,
        })
    
    return result


def get_user_progress_stats(user_id):
    """Get detailed progress statistics"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Calculate points progression
    milestone_points = {level: config['min_points'] 
                       for level, config in SKILL_LEVELS.items()}
    
    current_level = user.skill_level
    current_points = user.total_points
    
    # Find next milestone
    next_level = None
    points_to_next = 0
    
    for level, points in sorted(milestone_points.items(), 
                               key=lambda x: x[1]):
        if points > current_points:
            next_level = level
            points_to_next = points - current_points
            break
    
    return {
        'current_level': current_level,
        'current_points': current_points,
        'next_level': next_level,
        'points_to_next': points_to_next,
        'progress_percentage': (
            (current_points / milestone_points[next_level] * 100) 
            if next_level else 100
        ),
        'achievements_unlocked': len(user.achievements),
        'badges_earned': len(user.badges),
        'total_scans': len(user.scans),
        'total_quizzes': len(user.quiz_results),
        'current_streak': user.current_streak,
        'longest_streak': user.longest_streak,
    }


def generate_daily_challenge():
    """Generate a daily challenge for users"""
    challenges = [
        {
            'title': 'Phishing Detective',
            'description': 'Analyze 3 emails for phishing indicators',
            'points': 50,
            'requirement': 'complete_3_scans'
        },
        {
            'title': 'Quiz Champion',
            'description': 'Score 90%+ on any quiz',
            'points': 75,
            'requirement': 'quiz_score_90'
        },
        {
            'title': 'URL Master',
            'description': 'Scan 5 URLs and identify threats',
            'points': 60,
            'requirement': 'scan_5_urls'
        },
        {
            'title': 'Header Expert',
            'description': 'Analyze 3 email headers',
            'points': 55,
            'requirement': 'analyze_3_headers'
        },
        {
            'title': 'Learning Streak',
            'description': 'Complete 1 learning module',
            'points': 50,
            'requirement': 'complete_module'
        },
    ]
    
    # Rotate challenges daily
    import hashlib
    from datetime import datetime
    
    today = datetime.utcnow().date()
    challenge_index = int(
        hashlib.md5(str(today).encode()).hexdigest(), 16
    ) % len(challenges)
    
    return challenges[challenge_index]
