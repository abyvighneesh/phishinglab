"""
Comprehensive Email Analysis Module

Analyzes full emails for phishing indicators including:
- Header authentication checks (SPF, DKIM, DMARC)
- Email body analysis for suspicious content
- Attachment analysis
- Link analysis within email content
- Sender reputation checks
- Social engineering tactics

EDUCATIONAL PURPOSE ONLY
"""

import re
from email import message_from_string
from email.parser import Parser

def analyze_email(email_content):
    """
    Comprehensive email analysis for phishing indicators
    
    Args:
        email_content (str): Full email content (header + body)
        
    Returns:
        dict: Analysis results with risk score and indicators
    """
    result = {
        'from_address': '',
        'to_address': '',
        'subject': '',
        'date': '',
        'body_preview': '',
        'attachments': [],
        'links': [],
        'spf_result': 'Not Found',
        'dkim_result': 'Not Found',
        'dmarc_result': 'Not Found',
        'indicators': [],
        'risk_score': 0,
        'risk_level': 'Unknown'
    }
    
    try:
        # Parse email
        parser = Parser()
        msg = parser.parsestr(email_content)
        
        # Extract basic headers
        result['from_address'] = msg.get('From', '')
        result['to_address'] = msg.get('To', '')
        result['subject'] = msg.get('Subject', '')
        result['date'] = msg.get('Date', '')
        
        # Initialize risk tracking
        indicators = []
        risk_score = 0
        
        # ===== HEADER ANALYSIS =====
        auth_results = msg.get('Authentication-Results', '')
        result['spf_result'] = extract_spf_result(auth_results)
        result['dkim_result'] = extract_dkim_result(auth_results)
        result['dmarc_result'] = extract_dmarc_result(auth_results)
        
        # Check SPF failure
        if result['spf_result'] in ['fail', 'softfail', 'hardfail']:
            indicators.append({
                'type': 'SPF Authentication Failure',
                'severity': 'HIGH',
                'description': f'SPF check failed ({result["spf_result"]}) - sender may be spoofed',
                'risk_points': 35
            })
            risk_score += 35
        
        # Check DKIM failure
        if result['dkim_result'] == 'fail':
            indicators.append({
                'type': 'DKIM Authentication Failure',
                'severity': 'MEDIUM',
                'description': 'DKIM signature invalid - email may be tampered',
                'risk_points': 25
            })
            risk_score += 25
        
        # Check DMARC failure
        if result['dmarc_result'] == 'fail':
            indicators.append({
                'type': 'DMARC Policy Failure',
                'severity': 'HIGH',
                'description': 'DMARC authentication failed',
                'risk_points': 30
            })
            risk_score += 30
        
        # ===== SENDER ANALYSIS =====
        from_addr = result['from_address']
        from_domain = extract_domain(from_addr)
        
        # Check for domain mismatch with Return-Path
        return_path = msg.get('Return-Path', '')
        if from_addr and return_path:
            return_domain = extract_domain(return_path)
            if from_domain != return_domain and from_domain and return_domain:
                indicators.append({
                    'type': 'Domain Mismatch',
                    'severity': 'HIGH',
                    'description': f'From domain ({from_domain}) differs from Return-Path ({return_domain})',
                    'risk_points': 30
                })
                risk_score += 30
        
        # Check for typosquatting
        suspicious_patterns = [
            r'g00gle', r'goog1e', r'fac3book', r'micr0soft', r'paypa1',
            r'amaz0n', r'app1e', r'netf1ix', r'drop.?box', r'onedrive'
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, from_addr, re.IGNORECASE):
                indicators.append({
                    'type': 'Typosquatting Domain',
                    'severity': 'CRITICAL',
                    'description': 'Sender domain contains suspicious characters mimicking legitimate brands',
                    'risk_points': 40
                })
                risk_score += 40
                break
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
        if from_domain:
            for tld in suspicious_tlds:
                if from_domain.endswith(tld):
                    indicators.append({
                        'type': 'Suspicious Top-Level Domain',
                        'severity': 'MEDIUM',
                        'description': f'Email from suspicious TLD: {tld}',
                        'risk_points': 15
                    })
                    risk_score += 15
                    break
        
        # ===== SUBJECT ANALYSIS =====
        subject = result['subject'].lower()
        
        # Check for urgency/action keywords
        urgent_keywords = [
            r'urgent', r'action required', r'verify', r'confirm', r'immediately',
            r'update', r'alert', r'suspicious activity', r'click here', r'confirm identity'
        ]
        for keyword in urgent_keywords:
            if re.search(keyword, subject):
                indicators.append({
                    'type': 'Urgency/Action Keywords in Subject',
                    'severity': 'MEDIUM',
                    'description': f'Subject contains pressure tactic: "{keyword}"',
                    'risk_points': 15
                })
                risk_score += 15
                break
        
        # Check for account/security keywords
        account_keywords = [
            r'account', r'verify', r'billing', r'password', r'bank', r'payment',
            r'security alert', r'unusual activity'
        ]
        for keyword in account_keywords:
            if re.search(keyword, subject):
                indicators.append({
                    'type': 'Account/Security Alert Keywords',
                    'severity': 'MEDIUM',
                    'description': f'Subject uses account-related keywords that might be social engineering',
                    'risk_points': 12
                })
                risk_score += 12
                break
        
        # ===== BODY ANALYSIS =====
        body_text = get_email_body(msg)
        result['body_preview'] = body_text[:200]
        
        if body_text:
            # Check for suspicious links
            urls = extract_urls(body_text)
            result['links'] = urls
            
            suspicious_url_count = 0
            for url in urls:
                if is_suspicious_url(url, from_domain):
                    suspicious_url_count += 1
                    indicators.append({
                        'type': 'Suspicious Link',
                        'severity': 'HIGH',
                        'description': f'Email contains suspicious/shortened URL: {url[:50]}...',
                        'risk_points': 20
                    })
                    risk_score += 20
            
            # Check for credential requests
            credential_keywords = [
                r'enter password', r'confirm password', r'verify credentials',
                r'login credentials', r'username.*password', r'ssn', r'bank account',
                r'credit card', r'update payment'
            ]
            for keyword in credential_keywords:
                if re.search(keyword, body_text, re.IGNORECASE):
                    indicators.append({
                        'type': 'Credential Request',
                        'severity': 'CRITICAL',
                        'description': 'Email requests user to provide credentials or sensitive information',
                        'risk_points': 45
                    })
                    risk_score += 45
                    break
            
            # Check for HTML spoofing attempts
            if '<a href' in body_text and 'display:none' in body_text:
                indicators.append({
                    'type': 'HTML Spoofing Detected',
                    'severity': 'HIGH',
                    'description': 'Email contains hidden HTML content - link text may not match href',
                    'risk_points': 25
                })
                risk_score += 25
            
            # Check for poor grammar/spelling (common in phishing)
            grammar_issues = check_grammar_issues(body_text)
            if grammar_issues > 3:
                indicators.append({
                    'type': 'Poor Grammar/Spelling',
                    'severity': 'LOW',
                    'description': f'Email contains multiple spelling/grammar errors ({grammar_issues})',
                    'risk_points': 10
                })
                risk_score += 10
            
            # Check for scare tactics/threats
            threat_keywords = [
                r'will be', r'account.*suspend', r'will close', r'will deactivate',
                r'legal', r'lawsuit', r'charges', r'fraud'
            ]
            for keyword in threat_keywords:
                if re.search(keyword, body_text, re.IGNORECASE):
                    indicators.append({
                        'type': 'Threat/Scare Tactic',
                        'severity': 'MEDIUM',
                        'description': 'Email uses threats/scare tactics to pressure action',
                        'risk_points': 18
                    })
                    risk_score += 18
                    break
        
        # ===== ATTACHMENT ANALYSIS =====
        attachments = extract_attachments(msg)
        result['attachments'] = [att['filename'] for att in attachments]
        
        # Check for suspicious file extensions
        suspicious_extensions = ['.exe', '.bat', '.cmd', '.scr', '.vbs', '.js', '.jar']
        for att in attachments:
            filename = att['filename'].lower()
            for ext in suspicious_extensions:
                if filename.endswith(ext):
                    indicators.append({
                        'type': 'Suspicious Attachment',
                        'severity': 'CRITICAL',
                        'description': f'Email contains executable attachment: {att["filename"]}',
                        'risk_points': 50
                    })
                    risk_score += 50
                    break
        
        # Check for double extensions
        for att in attachments:
            filename = att['filename']
            if re.match(r'.*\.\w+\.\w+$', filename):
                indicators.append({
                    'type': 'Double Extension Attachment',
                    'severity': 'HIGH',
                    'description': f'Attachment uses double extension (e.g., document.pdf.exe): {filename}',
                    'risk_points': 35
                })
                risk_score += 35
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        result['risk_score'] = risk_score
        result['indicators'] = indicators
        
        # Determine risk level
        if risk_score >= 70:
            result['risk_level'] = 'CRITICAL'
        elif risk_score >= 50:
            result['risk_level'] = 'HIGH'
        elif risk_score >= 30:
            result['risk_level'] = 'MEDIUM'
        elif risk_score > 0:
            result['risk_level'] = 'LOW'
        else:
            result['risk_level'] = 'SAFE'
        
        # If no indicators found
        if not indicators:
            indicators.append({
                'type': 'No Major Issues Found',
                'severity': 'INFO',
                'description': 'Email appears legitimate, but always verify sender identity independently',
                'risk_points': 0
            })
        
    except Exception as e:
        result['indicators'].append({
            'type': 'Analysis Error',
            'severity': 'INFO',
            'description': f'Error parsing email: {str(e)}',
            'risk_points': 0
        })
    
    return result


def extract_domain(email_string):
    """Extract domain from email address"""
    if not email_string:
        return ''
    
    match = re.search(r'@([a-zA-Z0-9.-]+)', email_string)
    if match:
        return match.group(1).lower()
    return ''


def extract_spf_result(auth_results):
    """Extract SPF result from Authentication-Results"""
    if not auth_results:
        return 'Not Found'
    
    spf_match = re.search(r'spf=(\w+)', auth_results, re.IGNORECASE)
    if spf_match:
        return spf_match.group(1).lower()
    return 'Not Found'


def extract_dkim_result(auth_results):
    """Extract DKIM result from Authentication-Results"""
    if not auth_results:
        return 'Not Found'
    
    dkim_match = re.search(r'dkim=(\w+)', auth_results, re.IGNORECASE)
    if dkim_match:
        return dkim_match.group(1).lower()
    return 'Not Found'


def extract_dmarc_result(auth_results):
    """Extract DMARC result from Authentication-Results"""
    if not auth_results:
        return 'Not Found'
    
    dmarc_match = re.search(r'dmarc=(\w+)', auth_results, re.IGNORECASE)
    if dmarc_match:
        return dmarc_match.group(1).lower()
    return 'Not Found'


def get_email_body(msg):
    """Extract email body text from message"""
    body = ''
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    if isinstance(payload, bytes):
                        body = payload.decode('utf-8', errors='ignore')
                    else:
                        body = str(payload)
                    break
            elif content_type == 'text/html':
                payload = part.get_payload(decode=True)
                if payload:
                    if isinstance(payload, bytes):
                        body = payload.decode('utf-8', errors='ignore')
                    else:
                        body = str(payload)
                    # Continue to find plain text if available
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            if isinstance(payload, bytes):
                body = payload.decode('utf-8', errors='ignore')
            else:
                body = str(payload)
    
    return body


def extract_urls(text):
    """Extract URLs from email body"""
    url_pattern = r'https?://[^\s<>"\'\)]*'
    urls = re.findall(url_pattern, text)
    return list(set(urls))[:10]  # Return unique URLs, limit to 10


def is_suspicious_url(url, sender_domain):
    """Check if URL is suspicious"""
    suspicious_patterns = [
        r'bit\.ly', r'tinyurl', r'short\.link', r'ow\.ly',
        r'goo\.gl', r'custom-domain-spoofing',
    ]
    
    url_lower = url.lower()
    for pattern in suspicious_patterns:
        if re.search(pattern, url_lower):
            return True
    
    # Check if URL domain matches sender domain
    url_domain = re.search(r'https?://([^/]+)', url)
    if url_domain and sender_domain:
        url_host = url_domain.group(1).lower()
        if sender_domain not in url_host and url_host not in sender_domain:
            return True
    
    return False


def extract_attachments(msg):
    """Extract attachment information from message"""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    size = len(part.get_payload(decode=True)) if part.get_payload() else 0
                    attachments.append({
                        'filename': filename,
                        'size': size,
                        'content_type': part.get_content_type()
                    })
    
    return attachments


def check_grammar_issues(text):
    """Simple grammar issue detection"""
    issues = 0
    
    # Check for common misspellings
    misspellings = {
        r'\bclaik\b': 'click',
        r'\bconfrim\b': 'confirm',
        r'\bverify\b': 'verify',
        r'\bimmidiately\b': 'immediately',
        r'\buregent\b': 'urgent',
        r'\bproblme\b': 'problem'
    }
    
    for pattern in misspellings:
        if re.search(pattern, text, re.IGNORECASE):
            issues += 1
    
    # Check for multiple spaces
    if '  ' in text:
        issues += 1
    
    # Check for excessive punctuation
    if re.search(r'!{2,}', text) or re.search(r'\?{2,}', text):
        issues += 1
    
    return issues
