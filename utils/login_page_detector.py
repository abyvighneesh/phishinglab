"""
Fake Login Page Detector Module

Detects fake login pages by analyzing:
- Password input fields
- Form submission targets
- Suspicious JavaScript
- SSL certificate issues
- Brand impersonation

EDUCATIONAL PURPOSE ONLY - Safe detection, no exploitation
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import tldextract

# Known legitimate login page domains
LEGITIMATE_LOGIN_DOMAINS = {
    'google.com': ['accounts.google.com', 'myaccount.google.com'],
    'facebook.com': ['www.facebook.com', 'm.facebook.com'],
    'microsoft.com': ['login.microsoftonline.com', 'login.live.com'],
    'apple.com': ['appleid.apple.com'],
    'paypal.com': ['www.paypal.com'],
    'amazon.com': ['www.amazon.com'],
    'instagram.com': ['www.instagram.com'],
    'twitter.com': ['twitter.com', 'x.com']
}

# Brand keywords to detect impersonation
BRAND_KEYWORDS = [
    'google', 'gmail', 'facebook', 'microsoft', 'apple', 'paypal',
    'amazon', 'netflix', 'instagram', 'twitter', 'linkedin', 'dropbox',
    'bank', 'banking', 'chase', 'wellsfargo', 'bofa', 'citibank'
]

def detect_fake_login(url):
    """
    Detect if a URL hosts a fake login page
    
    Args:
        url (str): URL to analyze
        
    Returns:
        dict: Detection results with risk score and indicators
    """
    result = {
        'url': url,
        'has_login_form': False,
        'password_fields_count': 0,
        'form_action': 'Not Found',
        'external_submission': False,
        'suspicious_js': False,
        'ssl_valid': 'Unknown',
        'brand_impersonation': None,
        'indicators': [],
        'risk_score': 0,
        'risk_level': 'Unknown'
    }
    
    try:
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        result['url'] = url
        parsed_url = urlparse(url)
        
        # Extract domain
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        
        indicators = []
        risk_score = 0
        
        # Check 1: Protocol (HTTP vs HTTPS)
        if parsed_url.scheme != 'https':
            indicators.append({
                'type': 'Insecure Connection',
                'severity': 'HIGH',
                'description': 'Login page not using HTTPS - credentials would be sent unencrypted',
                'risk_points': 40
            })
            risk_score += 40
            result['ssl_valid'] = 'No SSL'
        else:
            result['ssl_valid'] = 'HTTPS Used'
        
        # Check 2: Try to fetch and analyze page (with safety measures)
        try:
            # Set a short timeout and user agent for safety
            headers = {
                'User-Agent': 'PhishLab-Scanner-Educational/1.0'
            }
            response = requests.get(url, headers=headers, timeout=5, verify=False, allow_redirects=True)
            
            if response.status_code == 200:
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for forms
                forms = soup.find_all('form')
                
                if forms:
                    result['has_login_form'] = True
                    
                    for form in forms:
                        # Check for password fields
                        password_inputs = form.find_all('input', {'type': 'password'})
                        result['password_fields_count'] += len(password_inputs)
                        
                        # Check form action
                        form_action = form.get('action', '')
                        if form_action:
                            result['form_action'] = form_action
                            
                            # Check if form submits to external domain
                            if form_action.startswith('http'):
                                form_domain = urlparse(form_action).netloc
                                if form_domain != parsed_url.netloc:
                                    result['external_submission'] = True
                                    indicators.append({
                                        'type': 'External Form Submission',
                                        'severity': 'CRITICAL',
                                        'description': f'Form submits credentials to external domain: {form_domain}',
                                        'risk_points': 50
                                    })
                                    risk_score += 50
                        
                        # Check for suspicious input names
                        suspicious_names = ['username', 'password', 'email', 'ssn', 'credit', 'card']
                        all_inputs = form.find_all('input')
                        for inp in all_inputs:
                            name = inp.get('name', '').lower()
                            if any(sus in name for sus in suspicious_names):
                                if not result['has_login_form']:
                                    result['has_login_form'] = True
                
                # If password field found
                if result['password_fields_count'] > 0:
                    indicators.append({
                        'type': 'Password Field Detected',
                        'severity': 'INFO',
                        'description': f'Found {result["password_fields_count"]} password field(s)',
                        'risk_points': 0
                    })
                
                # Check 3: Suspicious JavaScript
                scripts = soup.find_all('script')
                suspicious_js_patterns = [
                    r'document\.write',
                    r'eval\s*\(',
                    r'fromCharCode',
                    r'atob\s*\(',  # base64 decode
                    r'XMLHttpRequest',
                    r'\.submit\s*\(',
                ]
                
                for script in scripts:
                    script_content = script.string or ''
                    for pattern in suspicious_js_patterns:
                        if re.search(pattern, script_content):
                            result['suspicious_js'] = True
                            indicators.append({
                                'type': 'Suspicious JavaScript',
                                'severity': 'HIGH',
                                'description': f'Detected potentially malicious JS pattern: {pattern}',
                                'risk_points': 30
                            })
                            risk_score += 30
                            break
                    if result['suspicious_js']:
                        break
                
                # Check 4: Brand impersonation
                page_text = soup.get_text().lower()
                page_title = soup.title.string.lower() if soup.title else ''
                
                for brand in BRAND_KEYWORDS:
                    if brand in page_text or brand in page_title or brand in domain.lower():
                        # Check if domain is legitimate for this brand
                        is_legitimate = False
                        
                        for legit_brand, legit_domains in LEGITIMATE_LOGIN_DOMAINS.items():
                            if brand in legit_brand:
                                if any(parsed_url.netloc.endswith(ld) for ld in legit_domains):
                                    is_legitimate = True
                                    break
                        
                        if not is_legitimate and brand in page_text:
                            result['brand_impersonation'] = brand
                            indicators.append({
                                'type': 'Brand Impersonation',
                                'severity': 'CRITICAL',
                                'description': f'Page impersonates "{brand}" brand but hosted on suspicious domain',
                                'risk_points': 45
                            })
                            risk_score += 45
                            break
                
                # Check 5: Look for stolen/copied HTML
                meta_tags = soup.find_all('meta')
                for meta in meta_tags:
                    content = meta.get('content', '').lower()
                    # Check if meta tags reference different domain
                    for brand_domain in ['google.com', 'facebook.com', 'microsoft.com']:
                        if brand_domain in content and brand_domain not in domain:
                            indicators.append({
                                'type': 'Copied HTML Content',
                                'severity': 'HIGH',
                                'description': f'Page HTML references {brand_domain} but hosted elsewhere',
                                'risk_points': 35
                            })
                            risk_score += 35
                            break
        
        except requests.Timeout:
            indicators.append({
                'type': 'Connection Timeout',
                'severity': 'INFO',
                'description': 'Could not fetch page - connection timeout',
                'risk_points': 0
            })
        except requests.RequestException as e:
            indicators.append({
                'type': 'Connection Error',
                'severity': 'INFO',
                'description': f'Could not fetch page: {str(e)[:100]}',
                'risk_points': 0
            })
        
        # Check 6: Domain-based checks
        # Check for login-related keywords in non-legitimate domains
        login_keywords = ['login', 'signin', 'account', 'secure', 'verify']
        if any(kw in domain.lower() for kw in login_keywords):
            # Check if it's a known legitimate login domain
            is_known_legit = any(
                parsed_url.netloc.endswith(ld)
                for legit_domains in LEGITIMATE_LOGIN_DOMAINS.values()
                for ld in legit_domains
            )
            
            if not is_known_legit:
                indicators.append({
                    'type': 'Suspicious Login Domain',
                    'severity': 'HIGH',
                    'description': 'Domain contains login-related keywords but is not a known service',
                    'risk_points': 30
                })
                risk_score += 30
        
        # Check 7: Recently registered domain (simplified check)
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            indicators.append({
                'type': 'High-Risk TLD',
                'severity': 'MEDIUM',
                'description': f'Domain uses TLD commonly associated with phishing',
                'risk_points': 25
            })
            risk_score += 25
        
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
        
        # If no indicators, provide feedback
        if not indicators:
            indicators.append({
                'type': 'No Major Issues Found',
                'severity': 'INFO',
                'description': 'Page appears safe, but always verify URL matches official website',
                'risk_points': 0
            })
    
    except Exception as e:
        result['indicators'].append({
            'type': 'Analysis Error',
            'severity': 'INFO',
            'description': f'Error analyzing page: {str(e)}',
            'risk_points': 0
        })
    
    return result
