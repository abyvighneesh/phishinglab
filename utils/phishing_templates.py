"""
Phishing Email Templates Module

This module provides safe, educational phishing email templates
for demonstration and awareness training purposes only.

ETHICAL NOTICE: These templates are SIMULATED and not sent to anyone.
"""

PHISHING_TEMPLATES = [
    {
        'id': 1,
        'name': 'Fake Google Security Alert',
        'subject': '🔴 URGENT: Suspicious Activity Detected on Your Account',
        'from': 'security-alert@g00gle-security.com',
        'body': '''
Dear User,

We detected unusual sign-in activity from an unrecognized device in [Unknown Location].

📍 Location: Lagos, Nigeria
🕐 Time: 2 hours ago
📱 Device: Unknown Android Device

If this wasn't you, please VERIFY YOUR ACCOUNT IMMEDIATELY to prevent unauthorized access.

[VERIFY ACCOUNT NOW] ← Click here within 24 hours

Failure to verify may result in account suspension.

Thank you,
Google Security Team

---
Google LLC | 1600 Amphitheatre Parkway, Mountain View, CA 94043
        ''',
        'tactic': 'Urgency + Fear',
        'red_flags': [
            '❌ Misspelled domain: "g00gle-security.com" (0 instead of o)',
            '❌ Creates panic with "URGENT" and time pressure',
            '❌ Generic greeting "Dear User" instead of your name',
            '❌ Suspicious link button without showing actual URL',
            '❌ Threatens account suspension',
            '❌ Email from free/suspicious domain, not @google.com'
        ],
        'legitimate_action': 'Go directly to google.com and check Security settings. Never click links in suspicious emails.'
    },
    {
        'id': 2,
        'name': 'Fake Bank Account Suspension',
        'subject': 'Your Account Has Been Temporarily Suspended - Action Required',
        'from': 'no-reply@secure-bankofamerica.net',
        'body': '''
Dear Valued Customer,

We have temporarily suspended your Bank of America account due to unusual activity detected.

⚠️ ACCOUNT STATUS: SUSPENDED
📅 Suspension Date: January 21, 2026
🔒 Reason: Failed verification attempts

To restore full access to your account, please complete the verification process:

Step 1: Click the link below
Step 2: Enter your account credentials
Step 3: Verify your identity with SSN

[RESTORE ACCOUNT ACCESS]

Note: Failure to verify within 48 hours will result in permanent account closure and fund freezing.

For immediate assistance, call: +1-800-XXX-XXXX (Spoofed Number)

Best regards,
Bank of America Security Department
        ''',
        'tactic': 'Authority + Urgency + Loss Aversion',
        'red_flags': [
            '❌ Domain is "secure-bankofamerica.net" not "bankofamerica.com"',
            '❌ Creates fear of losing access to money',
            '❌ Asks for sensitive info (SSN) via link',
            '❌ Generic greeting instead of account holder name',
            '❌ Short deadline (48 hours) creates pressure',
            '❌ Suspicious phone number',
            '❌ Real banks NEVER ask for credentials via email'
        ],
        'legitimate_action': 'Call your bank using the official number on your card or statement. Login directly through the official website.'
    },
    {
        'id': 3,
        'name': 'Fake Instagram Security Alert',
        'subject': 'Someone tried to log into your account',
        'from': 'security@instagram-security-team.com',
        'body': '''
Hi there,

We noticed a login attempt to your Instagram account from a new device.

📱 Device: iPhone 13 Pro
📍 Location: Moscow, Russia
🕐 Time: 45 minutes ago

Was this you? If not, your account may be compromised.

[SECURE MY ACCOUNT] ← Click to review and change password

If you don't recognize this activity, click the link above to:
• Change your password immediately
• Review recent login activity
• Enable two-factor authentication

Note: Your account will be disabled in 24 hours if not verified.

Stay safe,
The Instagram Security Team

Instagram © 2026
        ''',
        'tactic': 'Impersonation + Fear + FOMO',
        'red_flags': [
            '❌ Suspicious domain: "instagram-security-team.com" not from Meta/Facebook',
            '❌ Generic greeting "Hi there" instead of username',
            '❌ Creates panic about account compromise',
            '❌ Threatens account disabling',
            '❌ Suspicious time pressure (24 hours)',
            '❌ Real Instagram emails come from @mail.instagram.com'
        ],
        'legitimate_action': 'Open the Instagram app directly or go to instagram.com. Check login activity in Settings > Security.'
    },
    {
        'id': 4,
        'name': 'Fake IT Department Email',
        'subject': 'URGENT: Email Quota Exceeded - Action Required',
        'from': 'it-support@company-helpdesk.com',
        'body': '''
Dear Employee,

This is an automated notification from the IT Department.

Your email mailbox has exceeded its storage quota (98% full).

Current Status:
✉️ Used: 49GB / 50GB
⚠️ Status: CRITICAL

To prevent email service interruption, you must verify your account and upgrade storage:

[VERIFY ACCOUNT & UPGRADE STORAGE]

Required Actions:
1. Verify your employee credentials
2. Confirm your department
3. Accept storage upgrade

This must be completed within 4 hours or your email account will be suspended.

Do not reply to this email. Use the link above.

IT Support Team
Company IT Department
        ''',
        'tactic': 'Impersonation + Technical Urgency + Authority',
        'red_flags': [
            '❌ Domain "company-helpdesk.com" is not official company domain',
            '❌ IT departments rarely send urgent quota warnings via email',
            '❌ Very short deadline (4 hours) creates panic',
            '❌ Asks to verify credentials via external link',
            '❌ "Do not reply" is suspicious - real IT provides contact info',
            '❌ Lacks official IT ticket number or contact information'
        ],
        'legitimate_action': 'Contact your IT department directly via phone or internal support portal. Never click links in urgent IT emails.'
    },
    {
        'id': 5,
        'name': 'Fake Package Delivery',
        'subject': 'Your Package Could Not Be Delivered - Rescheduling Required',
        'from': 'notifications@fedex-delivery-service.com',
        'body': '''
Dear Customer,

We attempted to deliver your package but nobody was available to receive it.

📦 Tracking Number: FX-8827491029
📅 Delivery Attempt: January 21, 2026
📍 Address: [Your address would appear here]

To reschedule your delivery:

[RESCHEDULE DELIVERY]

You will need to:
• Verify your shipping address
• Confirm your identity
• Pay a redelivery fee of $3.99

Package will be returned to sender if not rescheduled within 48 hours.

FedEx Delivery Services
Track | Support | FAQ
        ''',
        'tactic': 'Curiosity + Urgency + Small Payment Request',
        'red_flags': [
            '❌ Domain "fedex-delivery-service.com" is not official (should be fedex.com)',
            '❌ Unexpected delivery notification',
            '❌ Asks for payment via email link',
            '❌ Generic "Dear Customer" greeting',
            '❌ Creates urgency with 48-hour deadline',
            '❌ Real tracking numbers can be verified on official website'
        ],
        'legitimate_action': 'Go directly to fedex.com and enter the tracking number. Never pay delivery fees through email links.'
    }
]

def get_phishing_templates():
    """
    Returns all available phishing templates
    
    Returns:
        list: List of phishing template dictionaries
    """
    return PHISHING_TEMPLATES

def get_template_by_id(template_id):
    """
    Get a specific template by ID
    
    Args:
        template_id (int): Template ID
        
    Returns:
        dict: Template data or None if not found
    """
    for template in PHISHING_TEMPLATES:
        if template['id'] == template_id:
            return template
    return None

def get_all_red_flags():
    """
    Aggregate all red flags from all templates for educational purposes
    
    Returns:
        list: Unique list of all red flags
    """
    all_flags = []
    for template in PHISHING_TEMPLATES:
        all_flags.extend(template['red_flags'])
    return list(set(all_flags))
