# 🚀 PhishLab - Complete Setup & Run Instructions

## Welcome to PhishLab! 

This guide will help you set up and run the complete phishing simulation and defense framework in just 5 minutes.

---

## ✅ Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Command line/terminal access
- ✅ Web browser (Chrome, Firefox, Edge, Safari)
- ✅ Internet connection (for installing packages)

### Check Python Version
```bash
python --version
# Should show: Python 3.8.x or higher
```

If not installed, download from: https://www.python.org/downloads/

---

## 📥 Step 1: Navigate to Project Directory

Open your terminal/command prompt and navigate to the PhishLab directory:

```bash
cd d:\phishlab
```

Or wherever you have the project located.

---

## 📦 Step 2: Install Dependencies (2 minutes)

### Option A: Direct Installation (Recommended for testing)
```bash
pip install flask==3.0.0 requests==2.31.0 beautifulsoup4==4.12.2 python-whois==0.8.0 tldextract==5.1.1 Werkzeug==3.0.1
```

### Option B: From requirements.txt
```bash
pip install -r requirements.txt
```

### Option C: Using Virtual Environment (Recommended for development)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed flask-3.0.0 requests-2.31.0 beautifulsoup4-4.12.2 ...
```

---

## ▶️ Step 3: Run the Application (30 seconds)

Simply run:
```bash
python app.py
```

**You should see:**
```
============================================================
PhishLab: Ethical Phishing Simulation Framework
============================================================

ETHICAL DISCLAIMER:
This is an EDUCATIONAL tool for cybersecurity awareness.
No real phishing attacks are performed.
All simulations are safe and offline.

============================================================

Starting server at http://127.0.0.1:5000
Press CTRL+C to quit

 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.x:5000
```

**✅ Success!** The application is now running!

---

## 🌐 Step 4: Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

Or:
```
http://127.0.0.1:5000
```

**You should see:** The PhishLab landing page with navigation and module cards.

---

## 🎯 Step 5: Take a Quick Tour (5 minutes)

### 1️⃣ Try Phishing Simulation
- Click **"Explore Simulations"** button
- Select **"Fake Google Security Alert"**
- Read the simulated phishing email
- Review the red flags analysis
- Understand the social engineering tactics

### 2️⃣ Scan a Suspicious URL
- Click **"URL Scanner"** in navigation
- Enter: `https://g00gle-security.com`
- Click **"Scan URL"**
- Review the risk score and indicators
- Read defense recommendations

### 3️⃣ Test Your Knowledge
- Click **"Awareness"** in navigation
- Scroll to the quiz section
- Answer all 3 questions
- Check your score

**🎉 Congratulations! You've completed the PhishLab tour!**

---

## 🔧 Troubleshooting Guide

### Problem 1: "Python not found" or "python is not recognized"
**Solution:**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal/command prompt

### Problem 2: "ModuleNotFoundError: No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem 3: "Address already in use" or Port 5000 conflict
**Solution:**
Change the port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```
Then access: http://localhost:5001

### Problem 4: SSL Certificate Warnings
**Solution:**
This is normal for demonstration purposes. The application safely handles SSL verification for educational scanning. These warnings won't affect functionality.

### Problem 5: "Permission Denied" errors
**Solution:**
- On Windows: Run terminal as Administrator
- On Linux/Mac: Use `sudo pip install -r requirements.txt`
- Or use virtual environment (recommended)

### Problem 6: Slow URL scanning
**Solution:**
This is normal - the tool performs real domain lookups for educational purposes. Some operations may take 5-10 seconds.

---

## 🛑 Stopping the Application

Press `CTRL + C` in the terminal where the app is running.

You should see:
```
^C
Keyboard interrupt received, exiting.
```

---

## 🔄 Restarting the Application

Simply run again:
```bash
python app.py
```

---

## 🎓 What to Do Next

### For Learning:
1. ✅ Explore all 6 modules
2. ✅ Read the README.md for detailed documentation
3. ✅ Try different phishing templates
4. ✅ Analyze your own email headers
5. ✅ Take the security awareness quiz

### For Training:
1. ✅ Share with your security team
2. ✅ Use for employee awareness training
3. ✅ Customize phishing templates
4. ✅ Add organization-specific examples
5. ✅ Create training sessions around the tool

### For Development:
1. ✅ Review the code structure
2. ✅ Customize the templates
3. ✅ Add new phishing scenarios
4. ✅ Integrate with existing tools
5. ✅ Deploy to cloud platform

---

## 📊 Feature Testing Checklist

Test each module to ensure everything works:

- [ ] Home page loads correctly
- [ ] Navigation menu works
- [ ] Phishing Simulation displays templates
- [ ] Email Header Analyzer parses headers
- [ ] URL Scanner detects typosquatting
- [ ] Login Detector identifies forms
- [ ] Awareness page quiz works
- [ ] All defense recommendations appear
- [ ] Responsive design on mobile
- [ ] Charts and visualizations display

---

## 🔐 Security Notes

**This is a SAFE educational tool:**
- ✅ No actual phishing emails are sent
- ✅ No credentials are stored or harvested
- ✅ No malware is distributed
- ✅ All analysis is performed safely
- ✅ No unauthorized access attempts

**Always use responsibly:**
- ✅ For educational purposes only
- ✅ With proper authorization
- ✅ Following all applicable laws
- ✅ Respecting privacy and ethics

---

## 📚 Additional Resources

### Documentation:
- **README.md** - Complete documentation
- **QUICKSTART.md** - Quick start guide
- **PROJECT_SUMMARY.md** - Project overview
- **LICENSE** - Usage terms

### Learn More:
- CISA Phishing Guide: https://www.cisa.gov/phishing
- OWASP: https://owasp.org
- Anti-Phishing Working Group: https://apwg.org

### Report Phishing:
- APWG: reportphishing@apwg.org
- FBI IC3: https://ic3.gov
- FTC: https://reportfraud.ftc.gov

---

## 🎯 Quick Command Reference

```bash
# Navigate to project
cd d:\phishlab

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Run in background (Linux/Mac)
nohup python app.py &

# Check if running
netstat -ano | findstr :5000  # Windows
lsof -i :5000                  # Linux/Mac

# Stop application
CTRL + C
```

---

## ✨ Tips for Best Experience

1. **Use modern browser** - Chrome, Firefox, Edge, Safari
2. **Enable JavaScript** - Required for interactive features
3. **Use fullscreen** - Better visualization of charts
4. **Try all modules** - Each teaches different concepts
5. **Read explanations** - Understanding is key to defense
6. **Take the quiz** - Test your knowledge
7. **Share knowledge** - Help others stay safe

---

## 📞 Getting Help

### If you encounter issues:
1. Check this troubleshooting guide
2. Review error messages carefully
3. Check Python and package versions
4. Try reinstalling dependencies
5. Search error messages online
6. Open GitHub issue (if applicable)

### For questions:
- Read the full README.md
- Review inline code comments
- Check Python docstrings
- Consult Flask documentation

---

## 🎉 You're All Set!

PhishLab is now running and ready to use for cybersecurity education and awareness training.

**Remember:**
- Use ethically and legally
- For educational purposes only
- Help make the internet safer
- Spread security awareness

**Stay safe online! 🛡️**

---

## 📝 Quick Start Summary

```bash
# One-line setup (after installing Python):
cd d:\phishlab && pip install -r requirements.txt && python app.py

# Then open: http://localhost:5000
```

**That's it! Enjoy PhishLab!** 🎣🔒

---

*Last Updated: January 21, 2026*
*Version: 1.0.0*
*Status: Production Ready ✅*
