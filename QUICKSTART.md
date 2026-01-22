# PhishLab Quick Start Guide

## 🚀 Get Started in 3 Minutes!

### Step 1: Install Dependencies (1 minute)
```bash
cd phishlab
pip install -r requirements.txt
```

### Step 2: Run the Application (30 seconds)
```bash
python app.py
```

You should see:
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
```

### Step 3: Open in Browser (30 seconds)
Navigate to: **http://localhost:5000**

### Step 4: Explore Features (1 minute)
1. Click "Explore Simulations" to see fake phishing emails
2. Try the "URL Scanner" with test URL: `https://g00gle-security.com`
3. Take the Security Awareness Quiz

## 🎯 First-Time Tutorial

### Try This: Complete Phishing Analysis Workflow

**1. Simulate a Phishing Email (2 minutes)**
- Go to "Simulate" page
- Click "Fake Google Security Alert"
- Read the email and identify red flags
- Note the social engineering tactics used

**2. Analyze a Suspicious URL (3 minutes)**
- Go to "URL Scanner"
- Enter: `http://paypa1-secure.tk`
- Click "Scan URL"
- Review the risk score and indicators
- Read defense recommendations

**3. Test Your Knowledge (2 minutes)**
- Go to "Awareness" page
- Scroll to the quiz section
- Answer all 3 questions
- Check your score

**Congratulations! You've completed the PhishLab tutorial!** 🎉

## 🔧 Troubleshooting

### Issue: Module Not Found Error
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port Already in Use
Edit `app.py` line 87:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Issue: SSL Certificate Errors
This is normal for demonstration purposes. The tool safely handles SSL verification.

## 📚 Next Steps

1. **Read the full README.md** for detailed documentation
2. **Explore all modules** to understand phishing attack vectors
3. **Share with your team** for security awareness training
4. **Report any issues** via GitHub

## ⚠️ Remember

**This is an EDUCATIONAL tool only!**
- Never use for real phishing attacks
- Always act ethically and legally
- Use for learning and awareness training

---

**Need Help?** Open an issue on GitHub or contact the security education team.

**Stay Safe Online!** 🛡️
