"""
Educational Engine
Manages learning modules, resources, progress tracking, and certifications
"""

from datetime import datetime
from utils.models import (
    db, User, LearningModule, LearningResource, LearningProgress,
    CertificationQuiz, CertificationResult
)

# Default learning modules
DEFAULT_MODULES = [
    {
        'title': 'Phishing Fundamentals',
        'description': 'Learn what phishing is and how it works',
        'category': 'email-phishing',
        'difficulty': 'Beginner',
        'duration_minutes': 15,
        'content': '''
        <h2>What is Phishing?</h2>
        <p>Phishing is a cyber attack technique where attackers try to trick users
        into revealing sensitive information by impersonating trusted sources.</p>
        
        <h3>Common Phishing Methods:</h3>
        <ul>
            <li><strong>Email Phishing:</strong> Fraudulent emails mimicking legitimate companies</li>
            <li><strong>Spear Phishing:</strong> Targeted attacks against specific individuals</li>
            <li><strong>Whaling:</strong> Attacks targeting high-level executives</li>
            <li><strong>Smishing:</strong> Phishing via SMS text messages</li>
            <li><strong>Vishing:</strong> Phone-based social engineering</li>
        </ul>
        
        <h3>Why Phishing Works:</h3>
        <ul>
            <li>Exploits human psychology and trust</li>
            <li>Uses urgency and fear tactics</li>
            <li>Mimics legitimate services</li>
            <li>Requires only one person to fall for it</li>
        </ul>
        '''
    },
    {
        'title': 'Email Header Analysis',
        'description': 'Understand email headers and spot spoofed emails',
        'category': 'email-analysis',
        'difficulty': 'Intermediate',
        'duration_minutes': 20,
        'content': '''
        <h2>Email Header Analysis</h2>
        <p>Email headers contain valuable information about an email\'s origin and authenticity.</p>
        
        <h3>Key Fields to Check:</h3>
        <ul>
            <li><strong>From:</strong> Sender address (can be spoofed)</li>
            <li><strong>Return-Path:</strong> Where bounced emails go (more reliable)</li>
            <li><strong>Received:</strong> Server path email took</li>
            <li><strong>SPF/DKIM/DMARC:</strong> Authentication protocols</li>
        </ul>
        
        <h3>Red Flags:</h3>
        <ul>
            <li>Mismatched From and Return-Path addresses</li>
            <li>SPF/DKIM authentication failures</li>
            <li>Suspicious IP addresses in Received headers</li>
            <li>Multiple hops that don\'t make sense</li>
        </ul>
        '''
    },
    {
        'title': 'URL Analysis and Safety',
        'description': 'Learn to identify malicious and suspicious URLs',
        'category': 'url-analysis',
        'difficulty': 'Intermediate',
        'duration_minutes': 18,
        'content': '''
        <h2>URL Analysis</h2>
        <p>URLs are a common phishing attack vector. Learn to analyze them for threats.</p>
        
        <h3>URL Red Flags:</h3>
        <ul>
            <li>Typosquatting (g00gle.com instead of google.com)</li>
            <li>Long URLs with encoded parameters</li>
            <li>URL shorteners hiding true destination</li>
            <li>HTTPS issues or self-signed certificates</li>
            <li>Subdomains that confuse domain ownership</li>
        </ul>
        
        <h3>Best Practices:</h3>
        <ul>
            <li>Hover over links to see actual URL</li>
            <li>Check domain spelling carefully</li>
            <li>Be suspicious of shortened URLs</li>
            <li>Look for HTTPS and valid certificate</li>
            <li>Use URL scanning tools</li>
        </ul>
        '''
    },
    {
        'title': 'Social Engineering Tactics',
        'description': 'Understand psychologicalmethods used by attackers',
        'category': 'social-engineering',
        'difficulty': 'Intermediate',
        'duration_minutes': 22,
        'content': '''
        <h2>Social Engineering Tactics</h2>
        <p>Attackers use psychological manipulation to trick victims.</p>
        
        <h3>Common Tactics:</h3>
        <ul>
            <li><strong>Urgency:</strong> Create time pressure to bypass thinking</li>
            <li><strong>Authority:</strong> Impersonate authority figures</li>
            <li><strong>Fear:</strong> Threaten negative consequences</li>
            <li><strong>Greed:</strong> Offer unrealistic rewards</li>
            <li><strong>Scarcity:</strong> Limited availability claims</li>
            <li><strong>Familiarity:</strong> Pretend to know you</li>
        </ul>
        
        <h3>Defense Strategies:</h3>
        <ul>
            <li>Recognize emotional manipulation</li>
            <li>Take time to verify</li>
            <li>Use official channels</li>
            <li>Never share passwords</li>
            <li>Trust your instincts</li>
        </ul>
        '''
    },
    {
        'title': 'Attachment Security',
        'description': 'Learn to identify dangerous file attachments',
        'category': 'attachment-security',
        'difficulty': 'Beginner',
        'duration_minutes': 15,
        'content': '''
        <h2>Attachment Security</h2>
        <p>Email attachments are a primary malware delivery method.</p>
        
        <h3>Dangerous File Types:</h3>
        <ul>
            <li>Executables: .exe, .scr, .bat, .cmd</li>
            <li>Macros: .docm, .xlsm, .pptm</li>
            <li>Scripts: .vbs, .js, .ps1</li>
            <li>Archives: .zip, .rar (containing executables)</li>
        </ul>
        
        <h3>Security Practices:</h3>
        <ul>
            <li>Never open unexpected attachments</li>
            <li>Verify sender before opening</li>
            <li>Check file extension matches type</li>
            <li>Scan with antivirus first</li>
            <li>Use protected viewing modes</li>
        </ul>
        '''
    },
    {
        'title': 'Incident Response',
        'description': 'What to do if you suspect a phishing attack',
        'category': 'incident-response',
        'difficulty': 'Intermediate',
        'duration_minutes': 20,
        'content': '''
        <h2>Incident Response</h2>
        <p>Know the steps to take if you suspect phishing.</p>
        
        <h3>Immediate Actions:</h3>
        <ol>
            <li>Do NOT click links or download attachments</li>
            <li>Do NOT provide personal information</li>
            <li>Do NOT reply to suspicious emails</li>
            <li>Keep the email as evidence</li>
            <li>Report to IT security team</li>
        </ol>
        
        <h3>Reporting Process:</h3>
        <ol>
            <li>Forward to security team</li>
            <li>Report phishing to company systems</li>
            <li>Contact external authorities if needed</li>
            <li>Change passwords if compromised</li>
            <li>Monitor accounts for suspicious activity</li>
        </ol>
        
        <h3>Prevention Going Forward:</h3>
        <ul>
            <li>Enable multi-factor authentication</li>
            <li>Update passwords regularly</li>
            <li>Keep software updated</li>
            <li>Use password managers</li>
            <li>Report suspicious activities</li>
        </ul>
        '''
    },
    {
        'title': 'Advanced Phishing Detection',
        'description': 'Advanced techniques for spotting sophisticated attacks',
        'category': 'advanced-detection',
        'difficulty': 'Advanced',
        'duration_minutes': 25,
        'content': '''
        <h2>Advanced Phishing Detection</h2>
        <p>Sophisticated attackers use advanced techniques to bypass defenses.</p>
        
        <h3>Advanced Attack Methods:</h3>
        <ul>
            <li>Homograph attacks (l vs 1, O vs 0)</li>
            <li>HTTPS spoofing with valid certificates</li>
            <li>Brand impersonation and lookalike domains</li>
            <li>Business Email Compromise (BEC)</li>
            <li>AI-generated content and deepfakes</li>
        </ul>
        
        <h3>Detection Tools:</h3>
        <ul>
            <li>Email authentication (SPF, DKIM, DMARC)</li>
            <li>Machine learning filters</li>
            <li>Sandboxed analysis</li>
            <li>User behavior analytics</li>
            <li>Threat intelligence feeds</li>
        </ul>
        '''
    },
    {
        'title': 'Data Protection Best Practices',
        'description': 'Protect personal and organizational data',
        'category': 'data-protection',
        'difficulty': 'Intermediate',
        'duration_minutes': 18,
        'content': '''
        <h2>Data Protection Best Practices</h2>
        <p>Safeguard sensitive information in the workplace.</p>
        
        <h3>Essentials:</h3>
        <ul>
            <li>Use strong, unique passwords</li>
            <li>Enable multi-factor authentication</li>
            <li>Never share credentials</li>
            <li>Secure sensitive documents</li>
            <li>Lock screens when away</li>
            <li>Use VPN for public WiFi</li>
        </ul>
        
        <h3>Organizational Practices:</h3>
        <ul>
            <li>Follow data classification policies</li>
            <li>Encrypt sensitive data</li>
            <li>Limit access on need-to-know basis</li>
            <li>Audit access logs</li>
            <li>Dispose securely</li>
        </ul>
        '''
    }
]

# Certification quiz template
DEFAULT_CERTIFICATION_QUIZ = {
    'title': 'Phishing Detection Certification',
    'description': 'Comprehensive certification test for phishing defense experts',
    'passing_score': 80,
    'questions': [
        {
            'id': 1,
            'question': 'What is the primary goal of a phishing attack?',
            'options': [
                'To test network security',
                'To steal sensitive information',
                'To improve user awareness',
                'To backup data'
            ],
            'correct': 1
        },
        {
            'id': 2,
            'question': 'Which email header field is most reliable for verifying sender identity?',
            'options': [
                'From',
                'Return-Path',
                'Subject',
                'Date'
            ],
            'correct': 1
        },
        {
            'id': 3,
            'question': 'What does DMARC stand for?',
            'options': [
                'Data Mail Authentication Record Control',
                'Domain-based Message Authentication, Reporting and Conformance',
                'Domain Mail Authentication Response Check',
                'Direct Mail Authentication Review Code'
            ],
            'correct': 1
        },
        # Add more questions...
    ]
}


def create_default_modules():
    """Create default learning modules in database"""
    for module_data in DEFAULT_MODULES:
        existing = LearningModule.query.filter_by(
            title=module_data['title']
        ).first()
        
        if not existing:
            module = LearningModule(
                title=module_data['title'],
                description=module_data['description'],
                content=module_data['content'],
                category=module_data['category'],
                difficulty=module_data['difficulty'],
                duration_minutes=module_data['duration_minutes'],
                created_by='System',
                is_published=True
            )
            db.session.add(module)
    
    db.session.commit()


def get_user_learning_progress(user_id):
    """Get user's learning module progress"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    progress_records = LearningProgress.query.filter_by(
        user_id=user_id
    ).all()
    
    modules = LearningModule.query.all()
    
    result = {
        'total_modules': len(modules),
        'completed_modules': sum(1 for p in progress_records if p.is_completed),
        'in_progress_modules': sum(1 for p in progress_records if not p.is_completed),
        'modules': []
    }
    
    for module in modules:
        progress = next(
            (p for p in progress_records if p.module_id == module.id),
            None
        )
        
        result['modules'].append({
            'id': module.id,
            'title': module.title,
            'category': module.category,
            'difficulty': module.difficulty,
            'duration': module.duration_minutes,
            'progress': progress.progress_percentage if progress else 0,
            'completed': progress.is_completed if progress else False,
            'started': progress is not None
        })
    
    return result


def update_module_progress(user_id, module_id, progress_percentage):
    """Update user's progress on a learning module"""
    existing = LearningProgress.query.filter_by(
        user_id=user_id,
        module_id=module_id
    ).first()
    
    if not existing:
        existing = LearningProgress(
            user_id=user_id,
            module_id=module_id
        )
        db.session.add(existing)
    
    existing.progress_percentage = progress_percentage
    
    if progress_percentage >= 100:
        existing.is_completed = True
        existing.completed_at = datetime.utcnow()
    
    db.session.commit()
    return True


def get_learning_resources(category=None):
    """Get learning resources by category"""
    query = LearningResource.query
    
    if category:
        query = query.filter_by(category=category)
    
    resources = query.order_by(LearningResource.created_at.desc()).all()
    
    return [
        {
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'url': r.url,
            'type': r.resource_type,
            'category': r.category,
            'source': r.source,
            'is_external': r.is_external
        }
        for r in resources
    ]


def create_certification_result(user_id, quiz_id, score, passed):
    """Record certification quiz result"""
    import secrets
    
    result = CertificationResult(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        passed=passed,
        certificate_token=secrets.token_urlsafe(32) if passed else None
    )
    db.session.add(result)
    db.session.commit()
    
    return {
        'passed': passed,
        'score': score,
        'certificate_token': result.certificate_token,
        'completed_at': result.completed_at.isoformat()
    }


def get_user_certifications(user_id):
    """Get user's certifications"""
    results = CertificationResult.query.filter_by(
        user_id=user_id,
        passed=True
    ).all()
    
    return [
        {
            'id': r.id,
            'quiz_id': r.quiz_id,
            'score': r.score,
            'passed': r.passed,
            'completed_at': r.completed_at.isoformat(),
            'certificate_token': r.certificate_token
        }
        for r in results
    ]


def get_learning_stats():
    """Get overall learning platform statistics"""
    return {
        'total_modules': LearningModule.query.count(),
        'published_modules': LearningModule.query.filter_by(is_published=True).count(),
        'total_resources': LearningResource.query.count(),
        'total_certifications': CertificationQuiz.query.count(),
    }


def generate_learning_recommendations(user_id):
    """Generate personalized learning recommendations"""
    user = User.query.get(user_id)
    if not user:
        return []
    
    completed_modules = LearningProgress.query.filter_by(
        user_id=user_id,
        is_completed=True
    ).all()
    
    completed_ids = {p.module_id for p in completed_modules}
    
    # Recommend based on skill level
    recommendations = []
    
    if user.skill_level == 'Beginner':
        modules = LearningModule.query.filter(
            LearningModule.difficulty.in_(['Beginner', 'Intermediate']),
            ~LearningModule.id.in_(completed_ids)
        ).limit(3).all()
    elif user.skill_level == 'Intermediate':
        modules = LearningModule.query.filter(
            LearningModule.difficulty.in_(['Intermediate', 'Advanced']),
            ~LearningModule.id.in_(completed_ids)
        ).limit(3).all()
    else:
        modules = LearningModule.query.filter(
            ~LearningModule.id.in_(completed_ids)
        ).order_by(LearningModule.difficulty.desc()).limit(3).all()
    
    for module in modules:
        recommendations.append({
            'id': module.id,
            'title': module.title,
            'description': module.description,
            'difficulty': module.difficulty,
            'duration': module.duration_minutes,
            'reason': f'Recommended for {user.skill_level} learners'
        })
    
    return recommendations
