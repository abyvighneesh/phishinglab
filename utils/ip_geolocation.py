"""
IP Geolocation Detection Tool
Analyzes IP addresses for geographic location, ISP, and threat level
"""

import requests
import re
from datetime import datetime

def validate_ip_address(ip):
    """Validate if string is a valid IP address"""
    ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_pattern, ip) is not None


def get_ip_geolocation(ip_address):
    """
    Get geolocation data for IP address
    Uses free IP geolocation APIs
    """
    if not validate_ip_address(ip_address):
        return {
            'valid': False,
            'error': 'Invalid IP address format',
            'risk_indicators': []
        }
    
    # Check for private IPs
    private_ips = [
        '127.0.0.1',  # localhost
        '192.168',
        '10.',
        '172.16',
        '172.17',
        '172.18',
        '172.19',
        '172.20',
        '172.21',
        '172.22',
        '172.23',
        '172.24',
        '172.25',
        '172.26',
        '172.27',
        '172.28',
        '172.29',
        '172.30',
        '172.31'
    ]
    
    is_private = any(ip_address.startswith(private) for private in private_ips)
    
    if is_private:
        return {
            'valid': True,
            'ip_address': ip_address,
            'type': 'Private IP',
            'description': 'This is a private IP address used within local networks',
            'risk_level': 'low',
            'risk_score': 10,
            'indicators': ['Private network address']
        }
    
    try:
        # Try using ip-api.com (free tier, no API key needed)
        response = requests.get(
            f'http://ip-api.com/json/{ip_address}',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                return analyze_geolocation_data(ip_address, data)
        
        # Fallback to ipwhois.io
        response = requests.get(
            f'https://ipwho.is/{ip_address}',
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                'valid': True,
                'ip_address': ip_address,
                'country': data.get('country'),
                'country_code': data.get('country_code'),
                'city': data.get('city'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'isp': data.get('connection', {}).get('isp'),
                'type': data.get('type'),
                'mobile': data.get('is_mobile'),
                'proxy': data.get('is_proxy'),
                'vpn': data.get('is_vpn'),
                'tor': data.get('is_tor'),
                'risk_level': determine_risk_level(data),
                'risk_score': calculate_risk_score(data),
                'indicators': identify_risk_indicators(data)
            }
    
    except requests.exceptions.RequestException as e:
        return {
            'valid': True,
            'ip_address': ip_address,
            'error': f'Could not fetch geolocation: {str(e)}',
            'cached_warning': 'Using offline analysis only'
        }
    
    return {
        'valid': True,
        'ip_address': ip_address,
        'warning': 'Could not retrieve geolocation data',
        'risk_level': 'unknown'
    }


def analyze_geolocation_data(ip_address, data):
    """Analyze geolocation data for threats"""
    risk_indicators = identify_risk_indicators(data)
    risk_score = calculate_risk_score(data)
    
    return {
        'valid': True,
        'ip_address': ip_address,
        'country': data.get('country'),
        'country_code': data.get('countryCode'),
        'city': data.get('city'),
        'region': data.get('regionName'),
        'latitude': data.get('lat'),
        'longitude': data.get('lon'),
        'timezone': data.get('timezone'),
        'isp': data.get('isp'),
        'organization': data.get('org'),
        'as': data.get('as'),
        'risk_level': determine_risk_level(data),
        'risk_score': risk_score,
        'indicators': risk_indicators,
        'threat_types': identify_threat_types(data)
    }


def identify_risk_indicators(data):
    """Identify suspicious patterns in geolocation"""
    indicators = []
    
    # Check for VPN/Proxy
    if data.get('proxy') or data.get('vpn'):
        indicators.append('VPN/Proxy detected')
    
    # Check for Tor
    if data.get('tor'):
        indicators.append('Tor exit node detected')
    
    # Check for datacenter
    if data.get('mobile') is False and 'datacenter' in str(data.get('isp', '')).lower():
        indicators.append('Datacenter IP')
    
    # Check for suspicious country (rare in phishing context)
    high_risk_countries = ['KP', 'IR', 'SY']  # North Korea, Iran, Syria codes
    if data.get('countryCode') in high_risk_countries:
        indicators.append('High-risk country origin')
    
    return indicators


def identify_threat_types(data):
    """Identify specific threat types"""
    threats = []
    
    if data.get('proxy'):
        threats.append('Proxy Service')
    if data.get('vpn'):
        threats.append('VPN Usage')
    if data.get('tor'):
        threats.append('Tor Network')
    if 'datacenter' in str(data.get('isp', '')).lower():
        threats.append('Datacenter')
    if data.get('mobile'):
        threats.append('Mobile Network')
    
    return threats


def calculate_risk_score(data):
    """Calculate risk score 0-100"""
    score = 20  # Base score
    
    if data.get('proxy'):
        score += 25
    if data.get('vpn'):
        score += 20
    if data.get('tor'):
        score += 35
    if data.get('countryCode') in ['KP', 'IR', 'SY']:
        score += 15
    if 'datacenter' in str(data.get('isp', '')).lower():
        score += 10
    
    return min(score, 100)


def determine_risk_level(data):
    """Determine overall risk level"""
    score = calculate_risk_score(data)
    
    if score >= 70:
        return 'critical'
    elif score >= 50:
        return 'high'
    elif score >= 30:
        return 'medium'
    else:
        return 'low'


def extract_ips_from_email_headers(headers_text):
    """Extract IP addresses from email headers"""
    ip_pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    ips = re.findall(ip_pattern, headers_text)
    return list(set(ips))  # Remove duplicates


def analyze_email_ips(headers_text):
    """Analyze all IPs found in email headers"""
    ips = extract_ips_from_email_headers(headers_text)
    results = []
    
    for ip in ips:
        if not validate_ip_address(ip):
            continue
        
        result = get_ip_geolocation(ip)
        results.append({
            'ip': ip,
            'analysis': result
        })
    
    return {
        'ips_found': len(ips),
        'unique_ips': ips,
        'detailed_analysis': results,
        'suspicious_count': sum(1 for r in results if r['analysis'].get('risk_level') in ['high', 'critical'])
    }
