"""
Phone Number Validator
Detects spoofed, suspicious, and malicious phone numbers in emails
"""

import re
from datetime import datetime

# Common suspicious patterns in phone numbers used for phishing
SUSPICIOUS_PATTERNS = {
    'all_same_digit': r'^(\d)\1{6,}$',  # 1111111
    'sequential': r'^1234567|^9876543',  # Sequential digits
    'fake_patterns': r'^(555|666|777|888|999)',  # Commonly used fake numbers
}

# Known phishing phone number patterns
PHISHING_PHONE_CONTEXTS = {
    'urgent_support': ['support', 'help', 'security', 'account', 'verify'],
    'fake_banks': ['bank', 'paypal', 'amazon', 'apple', 'microsoft'],
    'emergency_calls': ['emergency', 'urgent', 'immediate', 'act now'],
}

# Country codes and patterns
COUNTRY_CODES = {
    'US': {'pattern': r'^(\+?1)?[2-9]\d{2}[2-9](?!11)\d{2}\d{4}$', 'dialcode': '+1', 'description': 'United States'},
    'UK': {'pattern': r'^(\+?44)?[0-9]{10,11}$', 'dialcode': '+44', 'description': 'United Kingdom'},
    'CA': {'pattern': r'^(\+?1)?[2-9]\d{2}[2-9](?!11)\d{6}$', 'dialcode': '+1', 'description': 'Canada'},
    'AU': {'pattern': r'^(\+?61)?[2-9]\d{8,9}$', 'dialcode': '+61', 'description': 'Australia'},
    'IN': {'pattern': r'^(\+?91)?[6-9]\d{9}$', 'dialcode': '+91', 'description': 'India'},
}


def validate_phone_format(phone_number):
    """Basic validation of phone number format"""
    # Remove common separators and spaces
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone_number)
    
    # Check if it contains only digits (after removing +)
    cleaned_digits = cleaned.replace('+', '')
    
    if not cleaned_digits.isdigit():
        return False, "Contains non-numeric characters"
    
    if len(cleaned_digits) < 7:
        return False, "Too short to be valid phone number"
    
    if len(cleaned_digits) > 15:
        return False, "Too long to be valid phone number"
    
    return True, "Valid format"


def detect_suspicious_patterns(phone_number):
    """Detect suspicious patterns in phone numbers"""
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone_number)
    suspicious_flags = []
    
    # Check for all same digits
    if re.match(SUSPICIOUS_PATTERNS['all_same_digit'], cleaned):
        suspicious_flags.append('All digits are the same')
    
    # Check for sequential digits
    if re.match(SUSPICIOUS_PATTERNS['sequential'], cleaned):
        suspicious_flags.append('Sequential digits detected')
    
    # Check for common fake number patterns
    if re.search(SUSPICIOUS_PATTERNS['fake_patterns'], cleaned):
        suspicious_flags.append('Known fake number pattern')
    
    # Check if number has too many 0s or 9s
    if cleaned.count('0') >= len(cleaned) * 0.5:
        suspicious_flags.append('Unusual distribution of 0s')
    
    if cleaned.count('9') >= len(cleaned) * 0.4:
        suspicious_flags.append('Unusual distribution of 9s')
    
    return suspicious_flags


def identify_country(phone_number):
    """Identify country from phone number format"""
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone_number)
    
    # Extract dial code if present
    dial_code_match = re.match(r'^\+?(\d{1,3})', phone_number)
    if dial_code_match:
        code = dial_code_match.group(1)
        # Map common dial codes
        dial_code_map = {
            '1': 'US/CA',
            '44': 'UK',
            '61': 'AU',
            '91': 'IN',
            '86': 'China',
            '81': 'Japan',
            '33': 'France',
            '49': 'Germany',
        }
        if code in dial_code_map:
            return dial_code_map[code]
    
    # Try to match country patterns
    for country, config in COUNTRY_CODES.items():
        if re.match(config['pattern'], phone_number):
            return country
    
    return 'Unknown'


def validate_country_format(phone_number, country_code='US'):
    """Validate phone number format for specific country"""
    if country_code not in COUNTRY_CODES:
        return False, f"Country code {country_code} not supported"
    
    pattern = COUNTRY_CODES[country_code]['pattern']
    
    if re.match(pattern, phone_number):
        return True, f"Valid {COUNTRY_CODES[country_code]['description']} format"
    
    return False, f"Does not match {COUNTRY_CODES[country_code]['description']} format"


def analyze_phone_context(phone_number, email_body='', email_sender=''):
    """Analyze phone number in context of email content"""
    risk_factors = []
    
    # Check if phone appears in urgent context
    urgent_keywords = ['urgent', 'immediate', 'act now', 'verify immediately', 'confirm now']
    if any(keyword in email_body.lower() for keyword in urgent_keywords):
        risk_factors.append('Appears in urgent/immediate context')
    
    # Check if sender claims to be from a known company
    company_keywords = ['support', 'team', 'service', 'department']
    company_names = ['amazon', 'apple', 'microsoft', 'google', 'facebook', 'paypal', 'bank']
    
    sender_lower = email_sender.lower()
    if any(name in sender_lower for name in company_names):
        risk_factors.append('Sender claims to be from known company')
    
    # Check if phone is linked to account verification
    verify_keywords = ['verify', 'confirm', 'validate', 'authenticate', 'authorization']
    if any(keyword in email_body.lower() for keyword in verify_keywords):
        risk_factors.append('Associated with account verification request')
    
    return risk_factors


def extract_phone_numbers(text):
    """Extract phone numbers from email text"""
    # Common phone number patterns
    patterns = [
        r'\+?[1-9]\d{1,14}',  # International format
        r'\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}',  # US format (555) 123-4567
        r'[0-9]{3}[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}',  # US format 555-123-4567
        r'\+[0-9]{1,3}\s?[0-9]{6,14}',  # International with spaces
    ]
    
    phones = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        phones.extend(found)
    
    return list(set(phones))  # Remove duplicates


def analyze_phone_number(phone_number, email_body='', email_sender=''):
    """Complete phone number analysis"""
    # Validate format
    is_valid, format_msg = validate_phone_format(phone_number)
    
    result = {
        'phone_number': phone_number,
        'cleaned': re.sub(r'[\s\-\(\)\+\.]', '', phone_number),
        'format_valid': is_valid,
        'format_message': format_msg,
        'country': identify_country(phone_number),
        'suspicious_patterns': detect_suspicious_patterns(phone_number),
        'context_risk_factors': analyze_phone_context(phone_number, email_body, email_sender),
        'risk_level': 'unknown',
        'risk_score': 0
    }
    
    # Calculate risk score
    risk_score = 0
    
    if not is_valid:
        risk_score += 30
    
    if result['suspicious_patterns']:
        risk_score += 25 * len(result['suspicious_patterns'])
    
    if result['context_risk_factors']:
        risk_score += 20 * len(result['context_risk_factors'])
    
    # Determine risk level
    if risk_score >= 70:
        result['risk_level'] = 'critical'
    elif risk_score >= 50:
        result['risk_level'] = 'high'
    elif risk_score >= 30:
        result['risk_level'] = 'medium'
    else:
        result['risk_level'] = 'low'
    
    result['risk_score'] = min(risk_score, 100)
    result['verdict'] = generate_verdict(result)
    
    return result


def generate_verdict(analysis):
    """Generate user-friendly verdict"""
    if analysis['risk_level'] == 'critical':
        return 'LIKELY PHISHING - Do not call this number'
    elif analysis['risk_level'] == 'high':
        return 'SUSPICIOUS - Verify through official company channels'
    elif analysis['risk_level'] == 'medium':
        return 'CAUTION - Check sender legitimacy before calling'
    else:
        return 'LOW RISK - But always verify sender identity'


def analyze_email_phones(email_body, email_sender=''):
    """Extract and analyze all phones in email"""
    phones = extract_phone_numbers(email_body)
    analyses = []
    
    for phone in phones:
        analysis = analyze_phone_number(phone, email_body, email_sender)
        analyses.append(analysis)
    
    return {
        'total_phones': len(phones),
        'unique_phones': list(set(phones)),
        'analyses': analyses,
        'critical_count': sum(1 for a in analyses if a['risk_level'] == 'critical'),
        'high_risk_count': sum(1 for a in analyses if a['risk_level'] == 'high'),
    }
