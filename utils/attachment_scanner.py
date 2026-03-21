"""
Attachment Scanner
Analyzes email attachments for phishing and malware indicators
"""

import re
import mimetypes
from datetime import datetime

# Dangerous file extensions commonly used in phishing/malware
DANGEROUS_EXTENSIONS = {
    'executable': ['.exe', '.scr', '.bat', '.cmd', '.com', '.pif', '.msi'],
    'script': ['.vbs', '.js', '.vbscript', '.ps1', '.powershell', '.scr'],
    'archive': ['.zip', '.rar', '.7z', '.gz', '.tar'],
    'macro': ['.doc', '.docm', '.xls', '.xlsm', '.ppt', '.pptm', '.docx'],
    'link': ['.lnk', '.url'],
}

# Safe file extensions
SAFE_EXTENSIONS = [
    '.pdf', '.txt', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx',
    '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.mp3', '.mp4', '.mov'
]

# Suspicious file name patterns
SUSPICIOUS_PATTERNS = {
    'urgency': r'(invoice|receipt|urgent|immediate|action|verify|confirm)',
    'mimicry': r'(invoice|receipt|payment|document|report)',
    'double_extension': r'\.[a-z]{2,4}\.[a-z]{2,4}$',  # .pdf.exe
    'hidden_extension': r'[^\s]*\s+\.[a-z]{3,4}$',  # spaces before extension
    'encoded_characters': r'%[0-9a-f]{2}',  # URL encoding
}

# Known malware file names
KNOWN_MALWARE_PATTERNS = [
    'locky',
    'wannacry',
    'notpetya',
    'emotet',
    'ransomware',
    'cryptolocker',
    'trickbot',
    'qbot',
    'cobalt',
    'konni',
]


def analyze_filename(filename):
    """Analyze filename for suspicious patterns"""
    result = {
        'filename': filename,
        'extension': '',
        'suspicious_flags': [],
        'risk_score': 0,
        'risk_level': 'low',
        'is_dangerous': False
    }
    
    # Extract extension
    parts = filename.rsplit('.', 1)
    if len(parts) == 2:
        extension = '.' + parts[1].lower()
        result['extension'] = extension
    else:
        result['suspicious_flags'].append('No file extension')
        result['risk_score'] += 15
    
    # Check for dangerous extensions
    for category, exts in DANGEROUS_EXTENSIONS.items():
        if result['extension'] in exts:
            result['is_dangerous'] = True
            result['suspicious_flags'].append(f'Dangerous {category} file: {result["extension"]}')
            if category in ['executable', 'script']:
                result['risk_score'] += 50
            elif category in ['macro', 'archive']:
                result['risk_score'] += 35
            elif category == 'link':
                result['risk_score'] += 30
    
    # Check for double extensions (e.g., document.pdf.exe)
    if re.search(SUSPICIOUS_PATTERNS['double_extension'], filename):
        result['suspicious_flags'].append('Double extension detected (possible masquerading)')
        result['risk_score'] += 40
        result['is_dangerous'] = True
    
    # Check for spaces before extension
    if re.search(SUSPICIOUS_PATTERNS['hidden_extension'], filename):
        result['suspicious_flags'].append('Unusual spacing before extension')
        result['risk_score'] += 20
    
    # Check for URL encoding
    if re.search(SUSPICIOUS_PATTERNS['encoded_characters'], filename):
        result['suspicious_flags'].append('URL-encoded characters in filename')
        result['risk_score'] += 15
    
    # Check for urgency keywords
    if re.search(SUSPICIOUS_PATTERNS['urgency'], filename.lower()):
        result['suspicious_flags'].append('Urgency-related filename')
        result['risk_score'] += 20
    
    # Check for known malware patterns
    filename_lower = filename.lower()
    for malware in KNOWN_MALWARE_PATTERNS:
        if malware in filename_lower:
            result['suspicious_flags'].append(f'Known malware pattern: {malware}')
            result['risk_score'] += 50
            result['is_dangerous'] = True
    
    # Check filename length (unusually long filenames may indicate obfuscation)
    if len(filename) > 100:
        result['suspicious_flags'].append('Unusually long filename (possible obfuscation)')
        result['risk_score'] += 10
    
    # Check for special characters that might bypass filters
    if re.search(r'[\x00-\x1f\x7f-\x9f]', filename):
        result['suspicious_flags'].append('Suspicious control characters in filename')
        result['risk_score'] += 25
    
    # Determine risk level
    if result['risk_score'] >= 70:
        result['risk_level'] = 'critical'
    elif result['risk_score'] >= 50:
        result['risk_level'] = 'high'
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    
    result['risk_score'] = min(result['risk_score'], 100)
    return result


def analyze_file_size(filename, size_bytes):
    """Analyze file size for anomalies"""
    result = {
        'filename': filename,
        'size_bytes': size_bytes,
        'size_mb': round(size_bytes / (1024 * 1024), 2),
        'anomalies': [],
        'risk_score': 0
    }
    
    # Get file extension
    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    
    # Check for typical file sizes
    typical_sizes = {
        'pdf': (1024, 50_000_000),  # 1KB to 50MB
        'doc': (100, 10_000_000),
        'xls': (100, 10_000_000),
        'zip': (1_000, 500_000_000),  # Can be larger
        'img': (100_000, 50_000_000),
    }
    
    # Check for unusually small files of potentially dangerous type
    if size_bytes < 10_000:
        if extension in DANGEROUS_EXTENSIONS['executable']:
            result['anomalies'].append('Unusually small executable file')
            result['risk_score'] += 15
    
    # Check for unusually large files
    if size_bytes > 500_000_000:  # > 500MB
        result['anomalies'].append('Very large file (> 500MB)')
        result['risk_score'] += 20
    
    # Check for zero-size files
    if size_bytes == 0:
        result['anomalies'].append('Zero-byte file')
        result['risk_score'] += 25
    
    return result


def analyze_attachment_context(filename, email_subject='', email_body=''):
    """Analyze attachment in context of email"""
    context_flags = []
    
    # Check for urgency+attachment combo
    urgency_keywords = ['urgent', 'immediate', 'action required', 'verify', 'confirm', 'act now']
    for keyword in urgency_keywords:
        if keyword in email_subject.lower() or keyword in email_body.lower():
            context_flags.append(f'Urgent language + attachment: {keyword}')
    
    # Check for payment-related attachments
    payment_keywords = ['invoice', 'payment', 'receipt', 'bill', 'charge']
    filename_lower = filename.lower()
    for keyword in payment_keywords:
        if keyword in filename_lower:
            if any(p in email_body.lower() for p in payment_keywords):
                context_flags.append(f'Payment-related attachment and email body')
    
    # Check for account verification requests
    verify_keywords = ['verify', 'confirm', 'update', 'authenticate', 'authorize']
    for keyword in verify_keywords:
        if keyword in email_body.lower():
            context_flags.append(f'Account request + attachment: {keyword}')
    
    # Check for unexpected attachments from unexpected sender domains
    # (This would need sender info)
    
    return context_flags


def analyze_attachment(filename, size_bytes=0, email_subject='', email_body=''):
    """
    Comprehensive attachment analysis
    """
    result = {
        'filename': filename,
        'analysis': {},
        'risk_level': 'low',
        'risk_score': 0,
        'verdict': '',
        'recommendations': []
    }
    
    # Analyze filename
    filename_analysis = analyze_filename(filename)
    result['analysis']['filename'] = filename_analysis
    result['risk_score'] += filename_analysis['risk_score']
    
    # Analyze file size
    if size_bytes > 0:
        size_analysis = analyze_file_size(filename, size_bytes)
        result['analysis']['size'] = size_analysis
        result['risk_score'] += size_analysis['risk_score']
    
    # Analyze context
    context_flags = analyze_attachment_context(filename, email_subject, email_body)
    result['analysis']['context'] = context_flags
    if context_flags:
        result['risk_score'] += len(context_flags) * 10
    
    # Determine overall risk level
    if result['risk_score'] >= 70:
        result['risk_level'] = 'critical'
    elif result['risk_score'] >= 50:
        result['risk_level'] = 'high'
    elif result['risk_score'] >= 30:
        result['risk_level'] = 'medium'
    
    result['risk_score'] = min(result['risk_score'], 100)
    
    # Generate verdict and recommendations
    if result['risk_level'] == 'critical':
        result['verdict'] = 'DO NOT OPEN - Likely malicious'
        result['recommendations'] = [
            'Do NOT open this attachment',
            'Report to your IT security team',
            'Delete the email',
            'Block the sender',
            'Run antivirus scan on your system'
        ]
    elif result['risk_level'] == 'high':
        result['verdict'] = 'SUSPICIOUS - Be very careful'
        result['recommendations'] = [
            'Do not open unless you expected this file',
            'Verify sender through separate communication',
            'Scan with antivirus before opening',
            'Check with IT if unsure',
            'Use sandbox/virtual machine if possible'
        ]
    elif result['risk_level'] == 'medium':
        result['verdict'] = 'CAUTION - Be careful'
        result['recommendations'] = [
            'Verify sender legitimacy',
            'Be cautious when opening',
            'Consider context of email',
            'Keep antivirus updated and enabled'
        ]
    else:
        result['verdict'] = 'Low risk, but be cautious'
        result['recommendations'] = [
            'Verify sender if unexpected',
            'Scan with antivirus as precaution',
            'Be cautious of unsolicited files'
        ]
    
    return result


def analyze_email_attachments(attachments_list, email_subject='', email_body=''):
    """
    Analyze all attachments in email
    attachments_list: list of dicts with 'filename' and 'size' keys
    """
    result = {
        'total_attachments': len(attachments_list),
        'attachments': [],
        'critical_count': 0,
        'high_risk_count': 0,
        'overall_risk_level': 'low',
        'summary': '',
        'recommendations': []
    }
    
    for attachment in attachments_list:
        filename = attachment.get('filename', '')
        size = attachment.get('size', 0)
        
        analysis = analyze_attachment(filename, size, email_subject, email_body)
        result['attachments'].append(analysis)
        
        if analysis['risk_level'] == 'critical':
            result['critical_count'] += 1
        elif analysis['risk_level'] == 'high':
            result['high_risk_count'] += 1
    
    # Determine overall risk
    if result['critical_count'] > 0:
        result['overall_risk_level'] = 'critical'
    elif result['high_risk_count'] > 0:
        result['overall_risk_level'] = 'high'
    
    # Generate summary
    if result['critical_count'] > 0:
        result['summary'] = f'⚠️ {result["critical_count"]} critical attachment(s) detected'
        result['recommendations'].append('DELETE THIS EMAIL - Do not open attachments')
    elif result['high_risk_count'] > 0:
        result['summary'] = f'⚠️ {result["high_risk_count"]} suspicious attachment(s) detected'
        result['recommendations'].append('Be very careful - verify before opening')
    elif result['total_attachments'] > 0:
        result['summary'] = f'📎 Email has {result["total_attachments"]} attachment(s)'
    else:
        result['summary'] = 'No attachments'
    
    return result


def get_attachment_safety_checklist():
    """Get safety checklist for attachments"""
    return {
        'before_opening': [
            'Verify you were expecting this attachment',
            'Confirm sender identity through separate communication',
            'Check file extension matches file type',
            'Be suspicious of double extensions',
            'Ensure antivirus is enabled and updated'
        ],
        'red_flags': [
            'Unexpected attachment from known contact',
            'Urgent language + attachment',
            'Suspicious filename or extension',
            'Request for password or sensitive info',
            'Archive files containing executables'
        ],
        'safe_practices': [
            'Save to quarantine folder first',
            'Scan before opening',
            'Use antivirus/malware scanner',
            'Open in sandbox if available',
            'Keep backups of important files',
            'Update software regularly'
        ]
    }
