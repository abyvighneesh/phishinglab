"""
Quiz System for Phishing Education
Provides quiz questions and puzzle solving based on phishing techniques
"""

from datetime import datetime
from utils.models import db, User, LearningModule, CertificationQuiz

# Quiz Questions based on Phishing Techniques
QUIZ_QUESTIONS = {
    'phishing_fundamentals': [
        {
            'id': 1,
            'type': 'multiple_choice',
            'question': 'What is the primary goal of a phishing attack?',
            'options': [
                'To crash a computer system',
                'To trick users into revealing sensitive information',
                'To delete files from a server',
                'To slow down internet speed'
            ],
            'correct_answer': 1,
            'difficulty': 'Beginner',
            'points': 10,
            'explanation': 'Phishing attacks aim to deceive users into disclosing confidential information like passwords, credit card numbers, or personal data.'
        },
        {
            'id': 2,
            'type': 'multiple_choice',
            'question': 'Which of these is an example of spear phishing?',
            'options': [
                'A mass email sent to all company employees',
                'A targeted email sent to a specific employee with personalized details',
                'An email sent to the CEO of a major corporation',
                'A text message with a suspicious link'
            ],
            'correct_answer': 1,
            'difficulty': 'Beginner',
            'points': 10,
            'explanation': 'Spear phishing is a targeted attack that uses personalized information about a specific individual or organization.'
        },
        {
            'id': 3,
            'type': 'true_false',
            'question': 'Legitimate companies will never ask you to confirm your password via email.',
            'options': ['True', 'False'],
            'correct_answer': 0,
            'difficulty': 'Beginner',
            'points': 5,
            'explanation': 'True. Legitimate companies never ask users to verify passwords, personal information, or payment details via email.'
        }
    ],
    'email_header_analysis': [
        {
            'id': 4,
            'type': 'multiple_choice',
            'question': 'Which email header field is most reliable for determining the true sender?',
            'options': [
                'From: field',
                'Return-Path: field',
                'Subject: field',
                'To: field'
            ],
            'correct_answer': 1,
            'difficulty': 'Intermediate',
            'points': 15,
            'explanation': 'The Return-Path field is more reliable because it indicates where bounce messages go and is harder to spoof.'
        },
        {
            'id': 5,
            'type': 'multiple_choice',
            'question': 'What does SPF stand for in email authentication?',
            'options': [
                'Sender Protection Framework',
                'Sender Policy Framework',
                'Security Protocol Framework',
                'Server Process Framework'
            ],
            'correct_answer': 1,
            'difficulty': 'Intermediate',
            'points': 15,
            'explanation': 'SPF (Sender Policy Framework) is an email authentication protocol that helps verify the sender\'s identity.'
        },
        {
            'id': 6,
            'type': 'true_false',
            'question': 'A mismatched From and Return-Path address is always a sign of phishing.',
            'options': ['True', 'False'],
            'correct_answer': 1,
            'difficulty': 'Intermediate',
            'points': 10,
            'explanation': 'False. While mismatches are suspicious and should be investigated, there can be legitimate reasons for differences.'
        }
    ],
    'url_analysis': [
        {
            'id': 7,
            'type': 'multiple_choice',
            'question': 'What is typosquatting?',
            'options': [
                'Clicking links too fast',
                'Registering domain names that are misspellings of legitimate domains',
                'Using a VPN to hide your location',
                'Clearing browser history frequently'
            ],
            'correct_answer': 1,
            'difficulty': 'Intermediate',
            'points': 15,
            'explanation': 'Typosquatting involves registering domain names with slight variations of popular domains to trick users into visiting malicious sites.'
        },
        {
            'id': 8,
            'type': 'multiple_choice',
            'question': 'Which URL is most likely to be legitimate?',
            'options': [
                'http://www.gogle.com',
                'http://www.g00gle.com',
                'https://www.google.com',
                'http://167.54.89.123/google'
            ],
            'correct_answer': 2,
            'difficulty': 'Intermediate',
            'points': 15,
            'explanation': 'https://www.google.com is legitimate. Look for: correct spelling, HTTPS protocol, and official domain names.'
        },
        {
            'id': 9,
            'type': 'true_false',
            'question': 'You should always trust URL shorteners like bit.ly because they are from trusted services.',
            'options': ['True', 'False'],
            'correct_answer': 1,
            'difficulty': 'Intermediate',
            'points': 10,
            'explanation': 'False. URL shorteners hide the actual destination. Always expand shortened URLs before clicking to see where they really go.'
        }
    ],
    'social_engineering': [
        {
            'id': 10,
            'type': 'multiple_choice',
            'question': 'What is the most common social engineering tactic?',
            'options': [
                'Physical break-ins',
                'Creating urgency and fear',
                'Changing server configurations',
                'Installing malware on servers'
            ],
            'correct_answer': 1,
            'difficulty': 'Advanced',
            'points': 20,
            'explanation': 'Creating urgency and fear is the most effective social engineering tactic because it bypasses rational decision-making.'
        },
        {
            'id': 11,
            'type': 'scenario',
            'question': 'You receive an email: "Your account has been compromised! Click here immediately to verify your identity." What should you do?',
            'options': [
                'Click the link immediately',
                'Call the company\'s official number from the statement or website',
                'Reply with your credentials to confirm',
                'Forward to all your contacts'
            ],
            'correct_answer': 1,
            'difficulty': 'Advanced',
            'points': 20,
            'explanation': 'Legitimate companies never request credentials via email. Always contact the company directly using official phone numbers or websites.'
        }
    ],
    'attachment_security': [
        {
            'id': 12,
            'type': 'multiple_choice',
            'question': 'Which file extension is most likely to contain malware?',
            'options': [
                '.txt (text file)',
                '.pdf (document)',
                '.exe (executable)',
                '.jpg (image)'
            ],
            'correct_answer': 2,
            'difficulty': 'Intermediate',
            'points': 15,
            'explanation': '.exe files are executable programs and are the most likely to contain malware. Be cautious with .exe, .bat, .scr, and .dll files.'
        },
        {
            'id': 13,
            'type': 'true_false',
            'question': 'Double extensions like "document.pdf.exe" are a common malware delivery technique.',
            'options': ['True', 'False'],
            'correct_answer': 0,
            'difficulty': 'Intermediate',
            'points': 10,
            'explanation': 'True. Attackers use double extensions to hide the true file type. Always check file properties to see the actual file type.'
        }
    ]
}

# Puzzle Challenges (Interactive)
PUZZLE_CHALLENGES = {
    'identify_phishing': {
        'title': 'Identify the Phishing Email',
        'description': 'Analyze these emails and identify which ones are phishing attempts',
        'difficulty': 'Beginner',
        'points': 25,
        'puzzles': [
            {
                'id': 1,
                'type': 'email_analysis',
                'email': {
                    'from': '"Bank Security" <security@mybank123.com>',
                    'subject': 'URGENT: Verify Your Account Now',
                    'content': 'Your account has been locked. Click here to verify your identity immediately.',
                    'links': ['http://mybank123.com/verify']
                },
                'red_flags': ['Domain mismatch', 'Urgency tactic', 'Requests credentials'],
                'is_phishing': True,
                'explanation': 'This is phishing. Banks never request verification via email, and the domain "mybank123.com" is suspicious.'
            },
            {
                'id': 2,
                'type': 'email_analysis',
                'email': {
                    'from': '"Amazon Support" <account-team@amazon.com>',
                    'subject': 'Your order #123-456-789 has shipped',
                    'content': 'Your order has shipped. You can track it here: [link to amazon.com/track]',
                    'links': ['https://amazon.com/track/123456']
                },
                'red_flags': [],
                'is_phishing': False,
                'explanation': 'This appears legitimate. From official Amazon domain, provides order details, and links to official site.'
            }
        ]
    },
    'url_safety_check': {
        'title': 'URL Safety Challenge',
        'description': 'Determine which URLs are safe to click',
        'difficulty': 'Intermediate',
        'points': 30,
        'puzzles': [
            {
                'id': 1,
                'url': 'https://www.paypa1.com/login',
                'is_safe': False,
                'reason': 'Typosquatting - "paypa1.com" mimics "paypal.com" with the number 1 replacing the letter l'
            },
            {
                'id': 2,
                'url': 'https://mail.google.com/mail',
                'is_safe': True,
                'reason': 'Official Google domain with HTTPS'
            },
            {
                'id': 3,
                'url': 'http://shop.amazon.com/products',
                'is_safe': False,
                'reason': 'Uses HTTP instead of HTTPS - no encryption'
            }
        ]
    },
    'header_detective': {
        'title': 'Email Header Detective',
        'description': 'Analyze email headers and find authentication issues',
        'difficulty': 'Advanced',
        'points': 40,
        'puzzles': [
            {
                'id': 1,
                'header': {
                    'From': 'CEO@company.com',
                    'Return-Path': 'bounce@suspicious-domain.net',
                    'SPF': 'FAIL',
                    'DKIM': 'FAIL',
                    'DMARC': 'FAIL'
                },
                'issues': ['Mismatched From and Return-Path', 'Failed SPF', 'Failed DKIM', 'Failed DMARC'],
                'risk_level': 'Critical',
                'explanation': 'Multiple authentication failures indicate this email is likely spoofed.'
            }
        ]
    }
}


def get_quiz_by_module(module_id):
    """Get quiz questions for a specific module"""
    module_map = {
        1: 'phishing_fundamentals',
        2: 'email_header_analysis',
        3: 'url_analysis',
        4: 'social_engineering',
        5: 'attachment_security',
    }
    
    module_key = module_map.get(module_id)
    if module_key in QUIZ_QUESTIONS:
        return QUIZ_QUESTIONS[module_key]
    return []


def get_puzzle_challenge(challenge_type):
    """Get puzzle challenges by type"""
    return PUZZLE_CHALLENGES.get(challenge_type, {})


def calculate_quiz_score(user_id, answers):
    """Calculate quiz score and award points"""
    total_points = 0
    correct_answers = 0
    
    for question_id, selected_answer in answers.items():
        # Find the question
        for category, questions in QUIZ_QUESTIONS.items():
            for q in questions:
                if q['id'] == question_id:
                    if q['correct_answer'] == selected_answer:
                        correct_answers += 1
                        total_points += q['points']
    
    return {
        'total_points': total_points,
        'correct_answers': correct_answers,
        'percentage': (correct_answers / len(answers) * 100) if answers else 0
    }


def submit_quiz_attempt(user_id, module_id, answers, score):
    """Record quiz attempt in database"""
    try:
        quiz_result = CertificationQuiz(
            user_id=user_id,
            module_id=module_id,
            answers=str(answers),
            score=score['percentage'],
            points_earned=score['total_points']
        )
        db.session.add(quiz_result)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error submitting quiz: {e}")
        return False


def get_user_quiz_stats(user_id):
    """Get user's quiz statistics"""
    quizzes = CertificationQuiz.query.filter_by(user_id=user_id).all()
    
    if not quizzes:
        return {
            'total_quizzes': 0,
            'average_score': 0,
            'total_points': 0
        }
    
    return {
        'total_quizzes': len(quizzes),
        'average_score': sum(q.score for q in quizzes) / len(quizzes),
        'total_points': sum(q.points_earned for q in quizzes)
    }
