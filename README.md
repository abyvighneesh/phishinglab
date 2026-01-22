# PhishLab: End-to-End Phishing Simulation & Defense Framework

![PhishLab Banner](static/images/banner.png)

## 🎯 Project Overview

**PhishLab** is a comprehensive educational cybersecurity web application designed to demonstrate phishing attack vectors, detection techniques, and defense strategies in a safe, controlled environment.

### ⚠️ ETHICAL DISCLAIMER

**THIS PROJECT IS STRICTLY FOR EDUCATIONAL AND AWARENESS PURPOSES ONLY.**

- ✅ Educational cybersecurity training
- ✅ Security awareness demonstrations
- ✅ Academic research and learning
- ❌ NO real phishing attacks
- ❌ NO credential harvesting
- ❌ NO malicious activities
- ❌ NO unauthorized access attempts

All simulations are **SAFE** and **OFFLINE**. This tool helps individuals and organizations understand phishing threats and improve their security posture.

---

## 🚀 Features

### 1. **Phishing Email Simulation**
- View realistic (but safe) phishing email templates
- Learn to identify red flags and social engineering tactics
- Understand urgency-based, authority-based, and fear-based attacks
- Templates include: Fake Google alerts, Bank warnings, Instagram security, IT department emails

### 2. **Email Header Analyzer**
- Parse and analyze email headers
- Check SPF, DKIM, and DMARC authentication
- Detect email spoofing attempts
- Identify domain mismatches and suspicious IPs
- Calculate phishing risk scores (0-100)

### 3. **URL Scanner**
- Analyze suspicious URLs for phishing indicators
- Detect typosquatting (g00gle vs google)
- Check domain age via WHOIS lookup
- Identify URL shorteners and suspicious TLDs
- Analyze HTTPS usage and redirects
- Calculate comprehensive risk scores

### 4. **Fake Login Page Detector**
- Scan web pages for fake login forms
- Detect password field usage
- Identify external form submissions
- Check for suspicious JavaScript
- Verify SSL certificates
- Detect brand impersonation

### 5. **Security Awareness Dashboard**
- Learn about different phishing types (email, spear, whaling, smishing, vishing)
- Best practices Do's and Don'ts
- Interactive security quiz
- Real-world case studies
- Reporting workflow guidelines

### 6. **Defense Strategy Engine**
- Personalized defense recommendations based on risk level
- Immediate action steps for detected threats
- Technical controls (MFA, email filtering, EDR)
- Incident response procedures
- Prevention measures and user training tips

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Beautiful Soup 4** - HTML parsing
- **Requests** - HTTP library
- **python-whois** - Domain age lookup
- **tldextract** - Domain parsing

### Frontend
- **HTML5**
- **CSS3** (Custom + Bootstrap 5)
- **JavaScript (ES6+)**
- **Bootstrap 5.3** - UI framework
- **Chart.js 4.4** - Data visualization

---

## 📁 Project Structure

```
phishlab/
│
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── templates/                      # HTML templates
│   ├── index.html                  # Landing page
│   ├── simulate.html               # Phishing simulation
│   ├── header_analyzer.html        # Email header analysis
│   ├── url_scanner.html            # URL scanning
│   ├── login_detector.html         # Login page detection
│   ├── awareness.html              # Security awareness
│   └── result.html                 # Generic results page
│
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css               # Custom styles
│   ├── js/
│   │   └── main.js                 # JavaScript utilities
│   └── images/                     # Image assets
│
└── utils/                          # Python utility modules
    ├── phishing_templates.py       # Phishing email templates
    ├── header_analysis.py          # Email header parsing
    ├── url_analysis.py             # URL scanning logic
    ├── login_page_detector.py      # Login page detection
    └── defense_engine.py           # Defense recommendations
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download Repository
```bash
git clone https://github.com/yourusername/phishlab.git
cd phishlab
```

Or download and extract the ZIP file.

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

---

## 🎮 Usage Guide

### Demo Flow

1. **Start at Home Page**
   - Review the educational disclaimer
   - Explore module descriptions
   - Understand the project goals

2. **Phishing Simulation**
   - Select a phishing template (Google, Bank, Instagram, etc.)
   - Read the fake phishing email
   - Identify red flags highlighted in the analysis
   - Learn about social engineering tactics used

3. **Email Header Analyzer**
   - Paste a suspicious email header
   - Click "Analyze Header"
   - Review SPF/DKIM/DMARC authentication results
   - Check detected indicators and risk score
   - Read defense recommendations

4. **URL Scanner**
   - Enter a suspicious URL
   - Click "Scan URL"
   - Review domain age, HTTPS status, typosquatting
   - Analyze risk score and indicators
   - Follow defense strategies

5. **Fake Login Detector**
   - Enter URL of suspected fake login page
   - Click "Detect Fake Login"
   - Review form analysis, SSL status, brand impersonation
   - Follow immediate action recommendations

6. **Security Awareness**
   - Learn about phishing types
   - Review Do's and Don'ts
   - Take the interactive quiz
   - Study real-world case examples
   - Learn how to report phishing

---

## 📊 Sample Test Data

### Test URLs for Scanner:
- **Fake Google:** `https://g00gle-security.com` (uses 0 instead of o)
- **Fake PayPal:** `http://paypa1-secure.tk` (HTTP + suspicious TLD)
- **URL Shortener:** `https://bit.ly/example`
- **Legitimate:** `https://google.com`

### Sample Email Header:
```
From: security@g00gle-alerts.com
To: user@example.com
Subject: URGENT: Verify Your Account
Return-Path: <spammer@suspicious.tk>
Authentication-Results: spf=fail dkim=fail dmarc=fail
Received: from unknown [192.168.1.1]
```

---

## 🔒 Security Features

### Input Validation
- All user inputs are sanitized
- SQL injection prevention (no database used)
- XSS prevention in HTML rendering
- URL validation before external requests

### Safe Analysis
- No actual phishing emails are sent
- External URL fetching uses timeouts
- SSL verification can be disabled for testing
- No credential storage or harvesting

### Rate Limiting (Recommended for Production)
Consider adding rate limiting middleware:
```python
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])
```

---

## 🧪 Testing

### Manual Testing
1. Test each module with provided sample data
2. Verify risk scores are calculated correctly
3. Check defense recommendations appear
4. Test responsive design on mobile devices

### Unit Testing (Future Enhancement)
```bash
pytest tests/
```

---

## 🔮 Future Enhancements

### Planned Features
- [ ] Machine learning-based phishing detection
- [ ] Email attachment analysis (sandbox)
- [ ] Real-time threat intelligence integration
- [ ] User progress tracking and certificates
- [ ] Multi-language support
- [ ] API for integration with other tools
- [ ] Docker containerization
- [ ] Database for logging and analytics
- [ ] Advanced reporting and dashboards
- [ ] Gamification elements

### Technical Improvements
- [ ] Add automated testing suite
- [ ] Implement caching for performance
- [ ] Add rate limiting
- [ ] Integrate with SIEM systems
- [ ] Add export to PDF functionality
- [ ] Implement user authentication
- [ ] Create admin dashboard

---

## 📚 Educational Resources

### Recommended Reading
- [CISA Phishing Guide](https://www.cisa.gov/phishing)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Anti-Phishing Working Group](https://apwg.org/)
- [Google's Security Blog](https://security.googleblog.com/)

### Reporting Phishing
- **Anti-Phishing Working Group:** reportphishing@apwg.org
- **FBI IC3:** https://ic3.gov
- **FTC:** https://reportfraud.ftc.gov

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code of Conduct
- Use this tool ethically and legally
- Follow responsible disclosure practices
- Respect privacy and data protection laws
- Contribute to cybersecurity education

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

**Note:** This software is provided for educational purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations.

---

## 👥 Authors & Acknowledgments

- **Project Creator:** Cybersecurity Education Team
- **Framework:** Flask, Bootstrap, Chart.js
- **Inspiration:** Real-world phishing attacks and defense strategies

### Special Thanks
- CISA for cybersecurity resources
- OWASP for security best practices
- Anti-Phishing Working Group
- Cybersecurity community

---

## 📞 Support & Contact

### Issues & Questions
- Open an issue on GitHub
- Email: security-education@example.com
- Documentation: See this README

### Stay Updated
- Star this repository for updates
- Watch for new releases
- Follow our blog for security tips

---

## ⚖️ Legal Notice

**IMPORTANT:** This tool is designed exclusively for:
- Educational purposes
- Security awareness training
- Academic research
- Authorized security testing

**PROHIBITED USES:**
- Real phishing attacks
- Unauthorized access attempts
- Credential harvesting
- Malware distribution
- Any illegal activities

**BY USING THIS SOFTWARE, YOU AGREE:**
- To use it only for ethical, legal, and educational purposes
- To comply with all applicable laws and regulations
- To not harm others or violate their privacy
- To take full responsibility for your actions

The creators and contributors assume no liability for misuse of this software.

---

## 🎓 Learning Objectives

After using PhishLab, users should be able to:

1. ✅ Identify common phishing email red flags
2. ✅ Understand social engineering tactics
3. ✅ Analyze email headers for authenticity
4. ✅ Detect suspicious URLs and domains
5. ✅ Recognize fake login pages
6. ✅ Implement strong defense strategies
7. ✅ Respond appropriately to phishing attempts
8. ✅ Educate others about phishing threats

---

## 🌟 Key Takeaways

### For Individuals:
- Always verify sender identity
- Think before you click
- Enable Multi-Factor Authentication
- Use password managers
- Report suspicious emails

### For Organizations:
- Implement security awareness training
- Deploy email authentication (SPF/DKIM/DMARC)
- Use email filtering solutions
- Conduct phishing simulations
- Establish clear reporting procedures

---

**Remember: The best defense against phishing is education and awareness!**

Stay safe online! 🛡️

---

*Last Updated: January 21, 2026*
*Version: 1.0.0*
