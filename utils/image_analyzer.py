"""
Image Analysis Tool
Detects suspicious images, manipulated content, and AI-generated images in emails
"""

import re
import base64
from datetime import datetime

# Common suspicious image indicators
SUSPICIOUS_IMAGE_INDICATORS = {
    'urgency': ['red', 'alert', 'warning', 'urgent', 'critical'],
    'spoofing': ['logo', 'badge', 'certification', 'verified'],
    'phishing': ['form', 'input', 'button', 'click here'],
}


def extract_images_from_html(html_content):
    """Extract image references from HTML email"""
    images = []
    
    # Find img tags
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    img_urls = re.findall(img_pattern, html_content, re.IGNORECASE)
    images.extend([{'type': 'img_tag', 'source': url} for url in img_urls])
    
    # Find background images
    bg_pattern = r'background[:-]?image\s*:\s*url\(["\']?([^)"\']+)["\']?\)'
    bg_urls = re.findall(bg_pattern, html_content, re.IGNORECASE)
    images.extend([{'type': 'background', 'source': url} for url in bg_urls])
    
    # Find base64 images
    base64_pattern = r'data:image/([^;]+);base64,([A-Za-z0-9+/=]+)'
    base64_images = re.findall(base64_pattern, html_content, re.IGNORECASE)
    images.extend([{'type': 'base64', 'format': fmt, 'data_length': len(data)} 
                   for fmt, data in base64_images])
    
    return images


def analyze_image_url(image_url):
    """Analyze image URL for suspicious patterns"""
    result = {
        'url': image_url,
        'is_external': False,
        'is_tracking_pixel': False,
        'suspicious_flags': [],
        'risk_score': 0,
        'risk_level': 'low'
    }
    
    # Check if external URL
    if image_url.startswith('http'):
        result['is_external'] = True
        result['suspicious_flags'].append('External image URL (not embedded)')
        result['risk_score'] += 10
    
    # Check for tracking pixels (1x1 images)
    if re.search(r'[?&](width|w|h|height)=1\b', image_url, re.IGNORECASE):
        result['is_tracking_pixel'] = True
        result['suspicious_flags'].append('Likely tracking pixel (1x1)')
        result['risk_score'] += 15
    
    # Check for suspicious parameters
    suspicious_params = ['redirect', 'track', 'click', 'log', 'monitor', 'spy']
    url_lower = image_url.lower()
    for param in suspicious_params:
        if param in url_lower:
            result['suspicious_flags'].append(f'Suspicious parameter detected: {param}')
            result['risk_score'] += 10
    
    # Check URL length (unusually long URLs may indicate encoding or obfuscation)
    if len(image_url) > 200:
        result['suspicious_flags'].append('Unusually long URL (possible encoding)')
        result['risk_score'] += 5
    
    # Check for suspicious domains
    suspicious_domains = ['analytics', 'tracking', 'pixel', 'clicker', 'beacon']
    for domain in suspicious_domains:
        if domain in url_lower:
            result['suspicious_flags'].append(f'Tracking-related domain: {domain}')
            result['risk_score'] += 15
    
    if result['risk_score'] >= 50:
        result['risk_level'] = 'high'
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    
    return result


def analyze_embedded_image(image_data):
    """Analyze embedded/base64 image"""
    result = {
        'is_embedded': True,
        'size_kb': len(image_data) / 1024,
        'suspicious_flags': [],
        'risk_score': 0,
        'risk_level': 'low'
    }
    
    # Check image size
    if len(image_data) > 500000:  # > 500KB
        result['suspicious_flags'].append('Large embedded image (> 500KB)')
        result['risk_score'] += 10
    
    # Very small images might be tracking pixels
    if len(image_data) < 100:  # < 100 bytes
        result['suspicious_flags'].append('Very small embedded image (possible tracking)')
        result['risk_score'] += 20
    
    return result


def detect_ai_generated_image_indicators(description=''):
    """
    Detect common indicators of AI-generated images
    Based on visual description/metadata
    """
    ai_indicators = []
    
    suspicious_patterns = [
        'perfectly smooth',
        'too perfect',
        'unrealistic lighting',
        'strange hands',
        'odd fingers',
        'floating objects',
        'impossible geometry',
        'watermark'
    ]
    
    description_lower = description.lower()
    for pattern in suspicious_patterns:
        if pattern in description_lower:
            ai_indicators.append(f'Potential AI generation sign: {pattern}')
    
    return ai_indicators


def detect_image_manipulation(description=''):
    """Detect signs of image manipulation"""
    manipulation_signs = []
    
    suspicious_patterns = [
        'blurred faces',
        'cut and paste',
        'edited',
        'modified',
        'deepfake',
        'inconsistent lighting',
        'shadow mismatch',
        'color correction'
    ]
    
    description_lower = description.lower()
    for pattern in suspicious_patterns:
        if pattern in description_lower:
            manipulation_signs.append(f'Possible manipulation: {pattern}')
    
    return manipulation_signs


def analyze_image_context(image_description='', email_context=''):
    """Analyze image in context of email"""
    context_flags = []
    
    # Check for urgency
    urgency_keywords = ['alert', 'warning', 'urgent', 'critical', 'immediate', 'action required']
    for keyword in SUSPICIOUS_IMAGE_INDICATORS['urgency']:
        if keyword in email_context.lower():
            context_flags.append(f'Image in urgent context: {keyword}')
    
    # Check for spoofing attempts
    spoofing_keywords = SUSPICIOUS_IMAGE_INDICATORS['spoofing']
    for keyword in spoofing_keywords:
        if keyword in image_description.lower():
            context_flags.append(f'Potential spoofing attempt: {keyword}')
    
    # Check for clickable images
    if 'button' in image_description.lower() or 'clickable' in image_description.lower():
        context_flags.append('Image appears to be clickable element')
    
    return context_flags


def analyze_email_images(html_content, email_context=''):
    """
    Comprehensive analysis of all images in email
    """
    images = extract_images_from_html(html_content)
    
    result = {
        'total_images': len(images),
        'images': [],
        'image_types': {
            'img_tag': 0,
            'background': 0,
            'base64': 0,
            'tracking_pixels': 0
        },
        'risk_score': 0,
        'risk_level': 'low',
        'summary': '',
        'red_flags': []
    }
    
    for image in images:
        image_analysis = {
            'type': image.get('type'),
            'analysis': {}
        }
        
        if image['type'] == 'base64':
            image_analysis['analysis'] = analyze_embedded_image(image.get('data_length', 0))
        elif image['type'] in ['img_tag', 'background']:
            image_analysis['analysis'] = analyze_image_url(image.get('source', ''))
        
        result['images'].append(image_analysis)
        result['image_types'][image['type']] += 1
        
        # Accumulate risks
        if 'risk_score' in image_analysis['analysis']:
            result['risk_score'] += image_analysis['analysis']['risk_score']
        
        if image_analysis['analysis'].get('is_tracking_pixel'):
            result['image_types']['tracking_pixels'] += 1
            result['red_flags'].append('Tracking pixel detected')
    
    # Normalize risk score
    if result['total_images'] > 0:
        result['risk_score'] = min(int(result['risk_score'] / result['total_images']), 100)
    
    # Determine overall risk level
    if result['risk_score'] >= 70:
        result['risk_level'] = 'critical'
    elif result['risk_score'] >= 50:
        result['risk_level'] = 'high'
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    
    # Generate summary
    if result['image_types']['tracking_pixels'] > 0:
        result['summary'] = f"Email contains {result['image_types']['tracking_pixels']} tracking pixel(s)"
    elif result['total_images'] == 0:
        result['summary'] = 'Email contains no images'
    else:
        result['summary'] = f"Email contains {result['total_images']} image(s)"
    
    return result


def get_image_red_flags():
    """Get list of image-related red flags"""
    return {
        'tracking_pixels': {
            'description': '1x1 pixel images used to track if email is opened',
            'risk': 'Privacy concern, confirms email address is monitored'
        },
        'external_images': {
            'description': 'Images hosted externally instead of embedded',
            'risk': 'Can be tracked or swapped for malicious versions'
        },
        'base64_images': {
            'description': 'Images embedded as base64 data',
            'risk': 'Can hide malicious code or be very large'
        },
        'image_maps': {
            'description': 'Images containing clickable areas',
            'risk': 'Can link to malicious sites'
        },
        'logo_spoofing': {
            'description': 'Images mimicking legitimate company logos',
            'risk': 'Part of well-crafted phishing attack'
        }
    }
