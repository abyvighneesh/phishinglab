"""
QR Code Analyzer
Detects and analyzes QR codes in emails and images for phishing threats
"""

import re
import base64
from urllib.parse import urlparse, parse_qs

# Common suspicious patterns in QR code URLs
SUSPICIOUS_QR_PATTERNS = {
    'shorteners': r'(bit\.ly|tinyurl|ow\.ly|short\.link|goo\.gl|amzn|rebrand)',
    'redirects': r'(redirect|redir|jump|click)',
    'obfuscation': r'(%3E|%3C|%25|%2F)',
}

# Known phishing QR hosting sites
PHISHING_QR_SITES = [
    'qrcode.com',
    'qr-code.store',
    'qrcode.ninja',
    'dynamic-qr.com',
]

# Encoding types that may indicate phishing
SUSPICIOUS_QR_ENCODINGS = [
    'EXECUTABLE',
    'X-EXECUTABLE',
    'PKCS12',
]


def detect_qr_codes_in_text(email_text):
    """Detect references to QR codes in email text"""
    qr_indicators = []
    qr_keywords = [
        'scan qr',
        'scan the qr code',
        'qr code',
        'scan code',
        'quick response code'
    ]
    
    text_lower = email_text.lower()
    for keyword in qr_keywords:
        if keyword in text_lower:
            qr_indicators.append(keyword)
    
    return list(set(qr_indicators))


def analyze_qr_url(url):
    """Analyze URL encoded in QR code"""
    result = {
        'url': url,
        'is_shortener': False,
        'has_redirect': False,
        'is_obfuscated': False,
        'is_suspicious': False,
        'risk_level': 'low',
        'risk_score': 0,
        'flags': []
    }
    
    # Check for URL shorteners
    if re.search(SUSPICIOUS_QR_PATTERNS['shorteners'], url.lower()):
        result['is_shortener'] = True
        result['flags'].append('URL shortener detected - destination obscured')
        result['risk_score'] += 25
    
    # Check for redirect patterns
    if re.search(SUSPICIOUS_QR_PATTERNS['redirects'], url.lower()):
        result['has_redirect'] = True
        result['flags'].append('Redirect URL pattern detected')
        result['risk_score'] += 20
    
    # Check for URL obfuscation
    if re.search(SUSPICIOUS_QR_PATTERNS['obfuscation'], url):
        result['is_obfuscated'] = True
        result['flags'].append('URL encoding/obfuscation detected')
        result['risk_score'] += 15
    
    # Parse URL and check domain
    try:
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Check for homograph attacks
        suspicious_domains = ['apple-id', 'paypal-login', 'amazon-account', 'google-verify']
        if any(sus in domain.lower() for sus in suspicious_domains):
            result['flags'].append('Suspicious domain pattern detected')
            result['risk_score'] += 30
        
        # Check for IP addresses instead of domain names
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            result['flags'].append('IP address used instead of domain')
            result['risk_score'] += 20
        
        # Check for suspicious port numbers
        if parsed.port and parsed.port not in [80, 443, 8080]:
            result['flags'].append(f'Unusual port number: {parsed.port}')
            result['risk_score'] += 15
    
    except Exception as e:
        result['flags'].append(f'Error parsing URL: {str(e)}')
        result['risk_score'] += 10
    
    # Determine risk level
    if result['risk_score'] >= 70:
        result['risk_level'] = 'critical'
        result['is_suspicious'] = True
    elif result['risk_score'] >= 50:
        result['risk_level'] = 'high'
        result['is_suspicious'] = True
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    else:
        result['risk_level'] = 'low'
    
    return result


def detect_qr_generator_service(qr_code_url=''):
    """Detect which service was used to generate QR code"""
    generators = {
        'qr-code-generator.com': 'QR Code Generator (legitimate)',
        'goqr.me': 'goQR.me (legitimate)',
        'qrcode.google.com': 'Google QR Code (legitimate)',
        'api.qrserver.com': 'QR Server (legitimate)',
        'dynamic-qr.com': 'Dynamic QR (potentially suspicious)',
        'qrcode.ninja': 'QR Code Ninja (potentially suspicious)',
    }
    
    if qr_code_url:
        for generator, desc in generators.items():
            if generator in qr_code_url.lower():
                return {'generator': generator, 'description': desc}
    
    return {'generator': 'Unknown', 'description': 'Could not identify QR generator'}


def extract_base64_images(email_html):
    """Extract base64 encoded images which may contain QR codes"""
    base64_pattern = r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)'
    matches = re.findall(base64_pattern, email_html)
    return matches


def analyze_qr_context(email_text, email_sender=''):
    """Analyze context of QR code in email"""
    context_flags = []
    
    # Check for urgency language
    urgency_keywords = ['urgent', 'immediately', 'now', 'verify', 'confirm', 'act now', 'limited time']
    for keyword in urgency_keywords:
        if keyword in email_text.lower():
            context_flags.append(f'Urgency language detected: "{keyword}"')
    
    # Check for payment requests near QR
    payment_keywords = ['payment', 'invoice', 'bill', 'charge', 'transfer', 'wire transfer']
    for keyword in payment_keywords:
        if keyword in email_text.lower():
            context_flags.append(f'Payment-related keyword found: "{keyword}"')
    
    # Check for account verification requests
    verify_keywords = ['verify', 'confirm', 'authorize', 'validate', 'authenticate']
    for keyword in verify_keywords:
        if keyword in email_text.lower():
            context_flags.append(f'Account verification request detected: "{keyword}"')
    
    # Check if sender claims to be from company
    company_keywords = ['google', 'apple', 'microsoft', 'amazon', 'paypal', 'bank']
    sender_lower = email_sender.lower()
    for company in company_keywords:
        if company in sender_lower:
            context_flags.append(f'Email claims to be from {company}')
    
    return context_flags


def analyze_qr_usage(email_text, email_sender='', qr_url=''):
    """
    Comprehensive analysis of QR code usage in email
    """
    result = {
        'has_qr_code': False,
        'qr_references': detect_qr_codes_in_text(email_text),
        'url_analysis': None,
        'context_flags': analyze_qr_context(email_text, email_sender),
        'risk_level': 'low',
        'risk_score': 0,
        'verdict': '',
        'recommendations': []
    }
    
    if result['qr_references']:
        result['has_qr_code'] = True
    
    # Analyze URL if provided
    if qr_url:
        result['url_analysis'] = analyze_qr_url(qr_url)
        result['risk_score'] = result['url_analysis']['risk_score']
        result['risk_level'] = result['url_analysis']['risk_level']
    
    # Add context risk
    if result['context_flags']:
        result['risk_score'] += len(result['context_flags']) * 15
    
    # Adjust overall risk level
    if result['risk_score'] >= 70:
        result['risk_level'] = 'critical'
    elif result['risk_score'] >= 50:
        result['risk_level'] = 'high'
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    
    # Generate verdict and recommendations
    if result['has_qr_code']:
        if result['risk_level'] == 'critical':
            result['verdict'] = 'LIKELY PHISHING - Do not scan QR code'
            result['recommendations'] = [
                'Do NOT scan this QR code',
                'Delete the email',
                'Report to your security team',
                'Block the sender'
            ]
        elif result['risk_level'] == 'high':
            result['verdict'] = 'SUSPICIOUS - Verify before scanning'
            result['recommendations'] = [
                'Verify sender through official channels',
                'Check if this is a legitimate request',
                'Look for alternative contact info',
                'Ask your IT department'
            ]
        elif result['risk_level'] == 'medium':
            result['verdict'] = 'CAUTION - Be careful before scanning'
            result['recommendations'] = [
                'Verify the sender is legitimate',
                'Check domain spelling carefully',
                'Use phone to verify before scanning'
            ]
        else:
            result['verdict'] = 'Low risk, but verify sender identity'
            result['recommendations'] = [
                'Verify sender identity',
                'Check for typos in domain',
                'Be cautious of unsolicited QR codes'
            ]
    
    result['risk_score'] = min(result['risk_score'], 100)
    return result


def get_qr_best_practices():
    """Get best practices for QR code safety"""
    return {
        'general': [
            'Only scan QR codes from trusted sources',
            'Verify QR code sender identity before scanning',
            'Be suspicious of unsolicited QR codes in emails',
            'Check the URL preview in QR scanner before opening'
        ],
        'email': [
            'Be wary of QR codes in unsolicited emails',
            'Legitimate companies usually don\'t use QR codes for urgent requests',
            'Verify requests through official channels',
            'Do not scan QR codes asking for payment'
        ],
        'payment': [
            'Never scan QR codes for payment confirmations from banks',
            'Verify payment requests through official app/website',
            'Use official company payment methods',
            'Contact company directly if payment request is unclear'
        ]
    }
