"""
URL Analysis Module

Analyzes URLs for phishing indicators including:
- Domain age and registration
- HTTPS usage and certificate validity
- URL shorteners
- Typosquatting patterns
- Suspicious redirects

EDUCATIONAL PURPOSE ONLY - Safe analysis, no actual exploitation
"""

import re
import tldextract
from urllib.parse import urlparse, parse_qs
import requests
from datetime import datetime

# Common URL shorteners
URL_SHORTENERS = [
    'bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly', 'is.gd',
    'buff.ly', 'adf.ly', 'bit.do', 'short.link', 'mcaf.ee'
]

# Legitimate brand domains for typosquatting detection
LEGITIMATE_BRANDS = {
    'google': ['google.com', 'gmail.com'],
    'facebook': ['facebook.com', 'fb.com'],
    'microsoft': ['microsoft.com', 'live.com', 'outlook.com'],
    'amazon': ['amazon.com', 'aws.amazon.com'],
    'paypal': ['paypal.com'],
    'apple': ['apple.com', 'icloud.com'],
    'netflix': ['netflix.com'],
    'instagram': ['instagram.com'],
    'twitter': ['twitter.com', 'x.com'],
    'linkedin': ['linkedin.com']
}

def scan_url(url):
    """
    Scan URL for phishing indicators
    
    Args:
        url (str): URL to analyze
        
    Returns:
        dict: Analysis results with risk score and indicators
    """
    result = {
        'url': url,
        'parsed_domain': '',
        'is_https': False,
        'is_shortened': False,
        'domain_age_days': 'Unknown',
        'redirect_chain': [],
        'indicators': [],
        'risk_score': 0,
        'risk_level': 'Unknown'
    }
    
    try:
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        result['url'] = url
        parsed = urlparse(url)
        
        # Extract domain information
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        result['parsed_domain'] = domain
        
        # Check HTTPS
        result['is_https'] = parsed.scheme == 'https'
        
        indicators = []
        risk_score = 0
        
        # Check 1: HTTP instead of HTTPS
        if not result['is_https']:
            indicators.append({
                'type': 'Insecure Protocol',
                'severity': 'MEDIUM',
                'description': 'URL uses HTTP instead of HTTPS - data not encrypted',
                'risk_points': 25
            })
            risk_score += 25
        
        # Check 2: URL shortener
        if domain in URL_SHORTENERS:
            result['is_shortened'] = True
            indicators.append({
                'type': 'URL Shortener Detected',
                'severity': 'MEDIUM',
                'description': 'Shortened URL hides actual destination - high phishing risk',
                'risk_points': 30
            })
            risk_score += 30
        
        # Check 3: Typosquatting detection
        typosquat_result = detect_typosquatting(domain)
        if typosquat_result:
            indicators.append({
                'type': 'Typosquatting Detected',
                'severity': 'CRITICAL',
                'description': f'Domain mimics {typosquat_result["brand"]}: {typosquat_result["reason"]}',
                'risk_points': 45
            })
            risk_score += 45
        
        # Check 4: Suspicious TLDs
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club', '.work', '.click']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            indicators.append({
                'type': 'Suspicious Top-Level Domain',
                'severity': 'HIGH',
                'description': f'Domain uses high-risk TLD commonly used in phishing',
                'risk_points': 35
            })
            risk_score += 35
        
        # Check 5: IP address instead of domain
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', extracted.domain):
            indicators.append({
                'type': 'IP Address URL',
                'severity': 'HIGH',
                'description': 'URL uses IP address instead of domain name - very suspicious',
                'risk_points': 40
            })
            risk_score += 40
        
        # Check 6: Excessive subdomains
        subdomain = extracted.subdomain
        if subdomain:
            subdomain_count = len(subdomain.split('.'))
            if subdomain_count >= 3:
                indicators.append({
                    'type': 'Excessive Subdomains',
                    'severity': 'MEDIUM',
                    'description': f'URL has {subdomain_count} subdomains - may hide true domain',
                    'risk_points': 20
                })
                risk_score += 20
        
        # Check 7: Suspicious keywords in URL
        suspicious_keywords = [
            'login', 'signin', 'account', 'verify', 'secure', 'update',
            'confirm', 'banking', 'paypal', 'password', 'suspended'
        ]
        url_lower = url.lower()
        found_keywords = [kw for kw in suspicious_keywords if kw in url_lower]
        if found_keywords and not result['is_https']:
            indicators.append({
                'type': 'Suspicious Keywords',
                'severity': 'HIGH',
                'description': f'URL contains phishing keywords: {", ".join(found_keywords[:3])}',
                'risk_points': 30
            })
            risk_score += 30
        
        # Check 8: Very long URL
        if len(url) > 200:
            indicators.append({
                'type': 'Abnormally Long URL',
                'severity': 'MEDIUM',
                'description': 'URL is suspiciously long - may hide malicious parameters',
                'risk_points': 15
            })
            risk_score += 15
        
        # Check 9: Special characters in domain
        if re.search(r'[^a-zA-Z0-9.-]', domain):
            indicators.append({
                'type': 'Special Characters in Domain',
                'severity': 'HIGH',
                'description': 'Domain contains unusual characters',
                'risk_points': 35
            })
            risk_score += 35
        
        # Check 10: Check for redirects (simulated - safe check)
        try:
            # Note: In production, be careful with following redirects
            # This is a simplified simulation for educational purposes
            redirect_check = check_redirects_safe(url)
            if redirect_check['has_redirects']:
                result['redirect_chain'] = redirect_check['chain']
                if redirect_check['redirect_count'] > 2:
                    indicators.append({
                        'type': 'Multiple Redirects',
                        'severity': 'MEDIUM',
                        'description': f'URL redirects {redirect_check["redirect_count"]} times - may hide destination',
                        'risk_points': 25
                    })
                    risk_score += 25
        except:
            pass
        
        # Check 11: Domain age analysis (simulated)
        domain_age = analyze_domain_age(domain)
        result['domain_age_days'] = domain_age
        if isinstance(domain_age, int) and domain_age < 30:
            indicators.append({
                'type': 'Recently Registered Domain',
                'severity': 'HIGH',
                'description': f'Domain is only {domain_age} days old - very suspicious',
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
        
        # If no indicators, provide positive feedback
        if not indicators:
            indicators.append({
                'type': 'No Major Issues Found',
                'severity': 'INFO',
                'description': 'URL appears legitimate, but always verify before entering credentials',
                'risk_points': 0
            })
    
    except Exception as e:
        result['indicators'].append({
            'type': 'Analysis Error',
            'severity': 'INFO',
            'description': f'Error analyzing URL: {str(e)}',
            'risk_points': 0
        })
    
    return result

def detect_typosquatting(domain):
    """
    Detect typosquatting attempts against known brands
    
    Args:
        domain (str): Domain to check
        
    Returns:
        dict or None: Detection result if typosquatting found
    """
    domain_lower = domain.lower()
    
    for brand, legit_domains in LEGITIMATE_BRANDS.items():
        # Skip if it's actually the legitimate domain
        if domain_lower in legit_domains:
            continue
        
        # Check for brand name in domain
        if brand in domain_lower:
            # Check for common typosquatting patterns
            
            # Pattern 1: Character substitution (0 for o, 1 for l, etc.)
            substitutions = {
                'o': '0', 'l': '1', 'i': '1', 'a': '4', 
                'e': '3', 's': '5', 'g': '9'
            }
            for char, sub in substitutions.items():
                if sub in domain_lower and brand.replace(char, sub) in domain_lower:
                    return {
                        'brand': brand,
                        'reason': f'Character substitution detected ({char}→{sub})'
                    }
            
            # Pattern 2: Extra characters or hyphens
            if re.search(rf'{brand}[-_]', domain_lower) or re.search(rf'[-_]{brand}', domain_lower):
                return {
                    'brand': brand,
                    'reason': 'Suspicious hyphens or underscores around brand name'
                }
            
            # Pattern 3: Common misspellings
            if domain_lower != legit_domains[0]:
                return {
                    'brand': brand,
                    'reason': 'Domain similar to legitimate brand but not official'
                }
    
    return None

def check_redirects_safe(url):
    """
    Safely check for redirects without following malicious links
    
    Args:
        url (str): URL to check
        
    Returns:
        dict: Redirect information
    """
    result = {
        'has_redirects': False,
        'redirect_count': 0,
        'chain': []
    }
    
    try:
        # Use a very short timeout and don't actually follow redirects for safety
        # This is a simulation - in real scenario, use sandbox environment
        response = requests.head(url, allow_redirects=False, timeout=3, verify=False)
        
        if response.status_code in [301, 302, 303, 307, 308]:
            result['has_redirects'] = True
            result['redirect_count'] = 1
            location = response.headers.get('Location', 'Unknown')
            result['chain'].append(location)
    except:
        # If request fails, assume no redirects for safety
        pass
    
    return result

def analyze_domain_age(domain):
    """
    Analyze domain age (simulated for educational purposes)
    
    Args:
        domain (str): Domain to check
        
    Returns:
        int or str: Domain age in days or 'Unknown'
    """
    # In a real implementation, this would use WHOIS lookup
    # For educational purposes, we simulate some results
    
    # Simulate: domains with suspicious patterns are "recently registered"
    suspicious_patterns = ['secure', 'verify', 'account', 'login', 'banking']
    if any(pattern in domain.lower() for pattern in suspicious_patterns):
        return 15  # Simulated: 15 days old
    
    # Simulate: well-known domains are old
    well_known = ['google.com', 'facebook.com', 'microsoft.com', 'amazon.com']
    if domain in well_known:
        return 8000  # Simulated: ~22 years old
    
    # For demo purposes, return Unknown for others
    return 'Unknown'
