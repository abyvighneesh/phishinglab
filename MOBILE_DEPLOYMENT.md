# 📱 PhishLab Mobile Deployment Guide

## **Option 1: Deploy on Render.com (Recommended - FREE)**

### Prerequisites
- GitHub account
- Render.com account (free tier)
- Your local code pushed to GitHub

### Steps:

1. **Push Your Code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/phishlab.git
   git push -u origin main
   ```

2. **Create Render.com Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Fill in the details:
     - **Name**: phishlab
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Region**: Choose closest to you

3. **Deploy!**
   - Click "Deploy"
   - Wait 3-5 minutes for build completion
   - Your app will be at: `https://phishlab-xxx.onrender.com`

4. **Access on Android**
   - Open any browser on your phone (Chrome, Firefox, Safari)
   - Visit: `https://phishlab-xxx.onrender.com`
   - Register → Verify Email → Login → Enjoy! 🎉

---

## **Option 2: Deploy on Railway.app**

1. Visit [railway.app](https://railway.app)
2. Click "Create New Project"
3. Select "Deploy from GitHub" (or use CLI)
4. Configure environment variables (set FLASK_ENV=production)
5. Railway auto-detects Flask and deploys automatically

**Access**: `https://your-project.railway.app`

---

## **Option 3: Deploy on Heroku (Still Free with Limitations)**

1. Install Heroku CLI
2. From your project directory:
   ```bash
   heroku login
   heroku create phishlab-app
   git push heroku main
   ```

3. Open: `https://phishlab-app.herokuapp.com`

---

## **Option 4: Local Network Access (Development)**

If you just want to test on Android via WiFi:

1. **Find your computer's IP**:
   - Windows: Run `ipconfig` → Find "IPv4 Address" (e.g., 192.168.x.x)
   - Mac/Linux: Run `ifconfig`

2. **Run Flask with network access**:
   ```bash
   python app.py --host=0.0.0.0 --port=5000
   ```

3. **On Android phone (same WiFi)**:
   - Open browser
   - Go to: `http://192.168.x.x:5000`

⚠️ **Note**: This works only on same WiFi, not over internet.

---

## **Mobile Optimization Checklist**

✅ Your app already has:
- Bootstrap 5 (responsive design)
- Mobile navbar toggle
- Viewport meta tag for mobile scaling

📱 **For best mobile experience, ensure**:
- Thumbs-friendly button sizes (min 44x44px)
- Responsive forms (already done ✓)
- Fast loading times (compress images if needed)
- Touch-friendly links/buttons spacing

---

## **Troubleshooting**

### App won't load on Android?
- Check internet connection
- Ensure HTTPS (Render/Railway provide this)
- Try clearing browser cache
- Open DevTools on browser (F12) to check console errors

### Email verification not working?
- Set SMTP_* environment variables in platform
- Check spam/junk folder
- Verify SMTP server details are correct

### Database issues?
- Render.com provides SQLite support (works great!)
- For production growth, upgrade to PostgreSQL ($7/month)

---

## **IMPORTANT: Before Going Live**

1. ✅ Set `FLASK_ENV=production` in environment variables
2. ✅ Change `SECRET_KEY` in app.py to a random string
3. ✅ Configure SMTP for email verification
4. ✅ Enable HTTPS cookies (automatic on Render/Railway)
5. ✅ Set strong database password if applicable

---

## **Mobile App Wrapper (Optional)**

To make it feel like a native Android app:
- Use [Cordova](https://cordova.apache.org/) or [React Native WebView](https://react-native-webview.js.org/)
- Or: Visit website → Browser menu → "Add to Home Screen"

---

## **Next Steps**

1. Choose a deployment platform (I recommend **Render.com**)
2. Push code to GitHub
3. Deploy and get your public URL
4. Open on Android phone
5. Register → Verify Email → Start Learning! 🚀

---

**Questions?** Check deployment platform's documentation or open a GitHub issue.
