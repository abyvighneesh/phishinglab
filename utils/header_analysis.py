"""
Email Header Analysis Module

Analyzes email headers for phishing indicators including:
- SPF, DKIM, DMARC authentication
- Email spoofing patterns
- Suspicious IP addresses
- Return-path mismatches

EDUCATIONAL PURPOSE ONLY
"""

import re
from email import message_from_string
from email.parser import Parser

def analyze_email_header(header_text):
    """
    Analyze email header for phishing indicators
    
    Args:
        header_text (str): Raw email header text
        
    Returns:
        dict: Analysis results with risk score and indicators
    """
    result = {
        'from_address': '',
        'return_path': '',
        'received_ips': [],
        'spf_result': 'Not Found',
        'dkim_result': 'Not Found',
        'dmarc_result': 'Not Found',
        'indicators': [],
        'risk_score': 0,
        'risk_level': 'Unknown'
    }
    
    try:
        # Parse email header
        parser = Parser()
        msg = parser.parsestr(header_text)
        
        # Extract From address
        from_header = msg.get('From', '')
        result['from_address'] = from_header
        
        # Extract Return-Path
        return_path = msg.get('Return-Path', '')
        result['return_path'] = return_path
        
        # Extract Received headers and IPs
        received_headers = msg.get_all('Received', [])
        ips = extract_ips_from_received(received_headers)
        result['received_ips'] = ips[:5]  # Limit to first 5 IPs
        
        # Check authentication results
        auth_results = msg.get('Authentication-Results', '')
        result['spf_result'] = extract_spf_result(auth_results)
        result['dkim_result'] = extract_dkim_result(auth_results)
        result['dmarc_result'] = extract_dmarc_result(auth_results)
        
        # Analyze for phishing indicators
        indicators = []
        risk_score = 0
        
        # Check 1: From/Return-Path mismatch
        if from_header and return_path:
            from_domain = extract_domain(from_header)
            return_domain = extract_domain(return_path)
            if from_domain != return_domain and from_domain and return_domain:
                indicators.append({
                    'type': 'Domain Mismatch',
                    'severity': 'HIGH',
                    'description': f'From domain ({from_domain}) differs from Return-Path domain ({return_domain})',
                    'risk_points': 30
                })
                risk_score += 30
        
        # Check 2: SPF failure
        if result['spf_result'] in ['fail', 'softfail', 'hardfail']:
            indicators.append({
                'type': 'SPF Authentication Failure',
                'severity': 'HIGH',
                'description': 'SPF check failed - sender may be spoofed',
                'risk_points': 35
            })
            risk_score += 35
        
        # Check 3: DKIM failure
        if result['dkim_result'] == 'fail':
            indicators.append({
                'type': 'DKIM Authentication Failure',
                'severity': 'MEDIUM',
                'description': 'DKIM signature invalid - email may be tampered',
                'risk_points': 25
            })
            risk_score += 25
        
        # Check 4: DMARC failure
        if result['dmarc_result'] == 'fail':
            indicators.append({
                'type': 'DMARC Policy Failure',
                'severity': 'HIGH',
                'description': 'DMARC authentication failed',
                'risk_points': 30
            })
            risk_score += 30
        
        # Check 5: Suspicious domains
        suspicious_patterns = [
            r'g00gle', r'fac3book', r'micr0soft', r'paypa1', 
            r'amaz0n', r'app1e', r'netf1ix', r'drop-?box'
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, from_header, re.IGNORECASE):
                indicators.append({
                    'type': 'Typosquatting Domain',
                    'severity': 'CRITICAL',
                    'description': f'Sender domain contains suspicious characters mimicking legitimate brands',
                    'risk_points': 40
                })
                risk_score += 40
                break
        
        # Check 6: Free email services for business emails
        free_email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com']
        from_domain = extract_domain(from_header)
        # Check if email claims to be from business but uses free service
        business_keywords = ['paypal', 'bank', 'amazon', 'microsoft', 'apple', 'security', 'admin', 'support']
        if from_domain in free_email_domains:
            for keyword in business_keywords:
                if keyword in from_header.lower():
                    indicators.append({
                        'type': 'Suspicious Free Email Service',
                        'severity': 'MEDIUM',
                        'description': f'Business/official email from free service ({from_domain})',
                        'risk_points': 20
                    })
                    risk_score += 20
                    break
        
        # Check 7: Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
        for tld in suspicious_tlds:
            if from_domain and from_domain.endswith(tld):
                indicators.append({
                    'type': 'Suspicious Top-Level Domain',
                    'severity': 'MEDIUM',
                    'description': f'Email from suspicious TLD: {tld}',
                    'risk_points': 15
                })
                risk_score += 15
                break
        
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
        
        # If no indicators found, provide positive feedback
        if not indicators:
            indicators.append({
                'type': 'No Major Issues Found',
                'severity': 'INFO',
                'description': 'Email headers appear legitimate, but always verify sender identity',
                'risk_points': 0
            })
        
    except Exception as e:
        result['indicators'].append({
            'type': 'Analysis Error',
            'severity': 'INFO',
            'description': f'Error parsing header: {str(e)}',
            'risk_points': 0
        })
    
    return result

def extract_ips_from_received(received_headers):
    """Extract IP addresses from Received headers"""
    ips = []
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    
    for header in received_headers:
        found_ips = re.findall(ip_pattern, str(header))
        ips.extend(found_ips)
    
    return ips

def extract_domain(email_string):
    """Extract domain from email address or header"""
    if not email_string:
        return ''
    
    # Match email pattern
    match = re.search(r'@([a-zA-Z0-9.-]+)', email_string)
    if match:
        return match.group(1).lower()
    return ''

def extract_spf_result(auth_results):
    """Extract SPF result from Authentication-Results header"""
    if not auth_results:
        return 'Not Found'
    
    spf_match = re.search(r'spf=(\w+)', auth_results, re.IGNORECASE)
    if spf_match:
        return spf_match.group(1).lower()
    return 'Not Found'

def extract_dkim_result(auth_results):
    """Extract DKIM result from Authentication-Results header"""
    if not auth_results:
        return 'Not Found'
    
    dkim_match = re.search(r'dkim=(\w+)', auth_results, re.IGNORECASE)
    if dkim_match:
        return dkim_match.group(1).lower()
    return 'Not Found'

def extract_dmarc_result(auth_results):
    """Extract DMARC result from Authentication-Results header"""
    if not auth_results:
        return 'Not Found'
    
    dmarc_match = re.search(r'dmarc=(\w+)', auth_results, re.IGNORECASE)
    if dmarc_match:
        return dmarc_match.group(1).lower()
    return 'Not Found'
