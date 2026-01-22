"""
Defense Strategy Engine

Generates defense recommendations and incident response steps
based on detected phishing indicators and risk scores.

EDUCATIONAL PURPOSE ONLY
"""

def generate_defense_tips(risk_score, indicators):
    """
    Generate defense recommendations based on risk assessment
    
    Args:
        risk_score (int): Risk score (0-100)
        indicators (list): List of detected indicators
        
    Returns:
        dict: Defense recommendations and response steps
    """
    defense_tips = {
        'immediate_actions': [],
        'prevention_measures': [],
        'technical_controls': [],
        'user_training': [],
        'incident_response': []
    }
    
    # Categorize risk level
    if risk_score >= 70:
        risk_level = 'CRITICAL'
    elif risk_score >= 50:
        risk_level = 'HIGH'
    elif risk_score >= 30:
        risk_level = 'MEDIUM'
    elif risk_score > 0:
        risk_level = 'LOW'
    else:
        risk_level = 'SAFE'
    
    # IMMEDIATE ACTIONS based on risk level
    if risk_level in ['CRITICAL', 'HIGH']:
        defense_tips['immediate_actions'] = [
            '🚨 DO NOT click any links or download attachments',
            '🚨 DO NOT enter any credentials or personal information',
            '🚨 Report this to your IT security team immediately',
            '🚨 Delete the email/close the webpage',
            '🚨 If you already clicked: Scan your device for malware',
            '🚨 If you entered credentials: Change passwords immediately'
        ]
    elif risk_level == 'MEDIUM':
        defense_tips['immediate_actions'] = [
            '⚠️ Exercise caution - do not trust this source',
            '⚠️ Verify sender identity through official channels',
            '⚠️ Do not click links - navigate directly to official website',
            '⚠️ Report suspicious activity to security team'
        ]
    else:
        defense_tips['immediate_actions'] = [
            '✓ Continue with normal security practices',
            '✓ Always verify sender identity before responding',
            '✓ When in doubt, contact the organization directly'
        ]
    
    # PREVENTION MEASURES
    defense_tips['prevention_measures'] = [
        '🔐 Enable Multi-Factor Authentication (MFA) on all accounts',
        '🔐 Use a password manager for unique, strong passwords',
        '🔐 Keep software and operating systems updated',
        '🔐 Install reputable antivirus/anti-malware software',
        '🔐 Use email filtering and spam protection',
        '🔐 Enable browser phishing protection features',
        '🔐 Be skeptical of urgent or threatening messages',
        '🔐 Verify URLs before clicking (hover over links)',
        '🔐 Check for HTTPS and valid SSL certificates',
        '🔐 Never share credentials via email or phone'
    ]
    
    # TECHNICAL CONTROLS
    defense_tips['technical_controls'] = [
        '🛡️ Implement SPF, DKIM, and DMARC email authentication',
        '🛡️ Deploy email security gateway with anti-phishing filters',
        '🛡️ Use DNS filtering to block known malicious domains',
        '🛡️ Implement endpoint detection and response (EDR)',
        '🛡️ Enable firewall and intrusion detection systems',
        '🛡️ Use sandboxing for suspicious attachments',
        '🛡️ Implement network segmentation',
        '🛡️ Deploy security awareness training platforms',
        '🛡️ Enable logging and monitoring for suspicious activities',
        '🛡️ Use conditional access policies based on risk'
    ]
    
    # USER TRAINING recommendations
    defense_tips['user_training'] = [
        '📚 Conduct regular phishing awareness training',
        '📚 Run simulated phishing exercises',
        '📚 Teach users to recognize common phishing tactics',
        '📚 Explain urgency and fear-based social engineering',
        '📚 Train users to verify sender identity',
        '📚 Educate on proper password hygiene',
        '📚 Demonstrate how to check URLs and certificates',
        '📚 Establish clear reporting procedures',
        '📚 Share real-world phishing examples',
        '📚 Create a security-first culture'
    ]
    
    # INCIDENT RESPONSE based on specific indicators
    if any(ind.get('severity') in ['CRITICAL', 'HIGH'] for ind in indicators):
        defense_tips['incident_response'] = [
            '🔍 INVESTIGATE: Check email logs for similar messages',
            '🔍 CONTAIN: Block sender domain and malicious URLs',
            '🔍 IDENTIFY: Determine if other users received same message',
            '🔍 ASSESS: Check if anyone clicked links or entered credentials',
            '🔍 REMEDIATE: Force password resets for affected accounts',
            '🔍 MONITOR: Watch for unusual account activity',
            '🔍 DOCUMENT: Record incident details for analysis',
            '🔍 NOTIFY: Alert security team and affected users',
            '🔍 REVIEW: Update security controls based on attack vector',
            '🔍 REPORT: File reports with relevant authorities if needed'
        ]
    else:
        defense_tips['incident_response'] = [
            '✓ Monitor for similar activity',
            '✓ Document the incident',
            '✓ Update security awareness training',
            '✓ Review and strengthen email filters'
        ]
    
    # Add specific recommendations based on indicator types
    indicator_types = [ind.get('type', '') for ind in indicators]
    
    # Domain-related issues
    if any(t in indicator_types for t in ['Domain Mismatch', 'Typosquatting Detected', 'Suspicious Top-Level Domain']):
        defense_tips['technical_controls'].insert(0, 
            '🛡️ PRIORITY: Implement domain name monitoring and typosquatting detection'
        )
    
    # Authentication failures
    if any(t in indicator_types for t in ['SPF Authentication Failure', 'DKIM Authentication Failure', 'DMARC Policy Failure']):
        defense_tips['technical_controls'].insert(0,
            '🛡️ PRIORITY: Review and strengthen email authentication policies (SPF/DKIM/DMARC)'
        )
    
    # Login page detection
    if any(t in indicator_types for t in ['Brand Impersonation', 'External Form Submission']):
        defense_tips['immediate_actions'].insert(0,
            '🚨 URGENT: This appears to be a credential harvesting attempt'
        )
        defense_tips['prevention_measures'].insert(0,
            '🔐 CRITICAL: Enable MFA immediately - compromised credentials less valuable with MFA'
        )
    
    return defense_tips

def get_risk_level_description(risk_score):
    """
    Get a human-readable description of the risk level
    
    Args:
        risk_score (int): Risk score (0-100)
        
    Returns:
        dict: Risk level information
    """
    if risk_score >= 70:
        return {
            'level': 'CRITICAL',
            'color': '#dc3545',
            'description': 'This is highly likely a phishing attempt. Do not interact with this content.',
            'icon': '🚨'
        }
    elif risk_score >= 50:
        return {
            'level': 'HIGH',
            'color': '#fd7e14',
            'description': 'Strong indicators of phishing detected. Exercise extreme caution.',
            'icon': '⚠️'
        }
    elif risk_score >= 30:
        return {
            'level': 'MEDIUM',
            'color': '#ffc107',
            'description': 'Some suspicious indicators found. Verify authenticity before proceeding.',
            'icon': '⚡'
        }
    elif risk_score > 0:
        return {
            'level': 'LOW',
            'color': '#17a2b8',
            'description': 'Minor concerns detected. Maintain normal security practices.',
            'icon': 'ℹ️'
        }
    else:
        return {
            'level': 'SAFE',
            'color': '#28a745',
            'description': 'No significant threats detected. Continue with standard security practices.',
            'icon': '✓'
        }

def get_security_checklist():
    """
    Get a comprehensive security checklist for users
    
    Returns:
        dict: Security checklist organized by category
    """
    return {
        'email_safety': [
            'Verify sender email address carefully',
            'Look for spelling errors in domain names',
            'Hover over links before clicking to see actual URL',
            'Check for generic greetings instead of your name',
            'Be suspicious of urgent or threatening language',
            'Don\'t trust "Sent from my iPhone" signatures',
            'Verify unexpected attachments before opening'
        ],
        'web_browsing': [
            'Always check URL in address bar',
            'Ensure HTTPS is used for login pages',
            'Look for valid SSL certificate (padlock icon)',
            'Beware of shortened URLs (bit.ly, etc.)',
            'Don\'t ignore browser security warnings',
            'Use bookmarks for frequently visited sites',
            'Keep browser and extensions updated'
        ],
        'password_security': [
            'Use unique passwords for each account',
            'Use password manager to generate strong passwords',
            'Enable Multi-Factor Authentication (MFA)',
            'Never share passwords via email',
            'Change passwords if breach suspected',
            'Use 12+ characters with mixed types',
            'Avoid personal information in passwords'
        ],
        'account_protection': [
            'Enable MFA on all critical accounts',
            'Monitor account activity regularly',
            'Review connected apps and permissions',
            'Set up security alerts',
            'Use biometric authentication when available',
            'Keep recovery information updated',
            'Log out when using shared computers'
        ],
        'reporting': [
            'Report suspicious emails to IT security',
            'Forward phishing emails to reportphishing@apwg.org',
            'Report to FBI IC3 if financial loss occurred',
            'Alert your bank if banking credentials compromised',
            'Document incident details',
            'Help others learn from your experience'
        ]
    }
