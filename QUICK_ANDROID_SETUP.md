# 🚀 Quick Start: PhishLab on Android (5 minutes)

## **Easiest Method: Render.com Deploy**

### 1️⃣ **Prepare Code (2 minutes)**
```bash
# Make sure you have git installed, then:
git init
git add .
git commit -m "Initial commit - PhishLab"
git remote add origin https://github.com/YOUR_USERNAME/phishlab.git
git push -u origin main
```

### 2️⃣ **Deploy on Render (2 minutes)**
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Click "New +" → "Web Service"
- Select your phishlab repository
- Set:
  - **Start Command**: `gunicorn app:app`
- Click "Deploy"

### 3️⃣ **Access on Android (1 minute)**
- Wait for build (shows "Live" status)
- Copy the URL: `https://phishlab-xxxxx.onrender.com`
- Open in Android browser
- **Done!** ✅

---

## **What You Get**
✅ Public HTTPS link (works from anywhere)  
✅ Auto-restarts if it crashes  
✅ Free SSL certificate  
✅ Mobile responsive design  
✅ Email verification working  

---

## **Alternative: Demo on Local WiFi** (No deploy needed)
```bash
python app.py --host=0.0.0.0 --port=5000
```
Then on Android phone (same WiFi):
- Open browser → `http://[YOUR_PC_IP]:5000`
- Example: `http://192.168.1.10:5000`

⚠️ Only works while your PC is running, only on same WiFi

---

## **FAQ**

**Q: Do I need an app?**  
A: No! Browser is enough. Your app is already responsive.

**Q: Is it secure?**  
A: Yes! Render provides HTTPS encryption.

**Q: Can I use my own domain?**  
A: Yes! ($0.50/month on Render)

**Q: Data saved on phone?**  
A: No, all data stored on server (you can access from multiple devices)

---

**Need help?** See `MOBILE_DEPLOYMENT.md` for detailed guide.
