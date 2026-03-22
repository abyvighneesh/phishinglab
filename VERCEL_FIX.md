# 🚀 PhishLab Vercel Deployment Fix

## ⚠️ What Was Wrong
Your Flask app was using `app.run()` which doesn't work on Vercel's serverless platform. Vercel expected a WSGI-compatible application.

## ✅ What I Fixed
1. ✅ Created `vercel.json` - Vercel configuration
2. ✅ Created `api/index.py` - Serverless entry point (WSGI handler)
3. ✅ Updated `requirements.txt` - Added gunicorn and wsgiref
4. ✅ Modified `app.py` - Debug mode only on development
5. ✅ Created `.vercelignore` - Ignore unnecessary files

## 🔧 How to Deploy (Updated Steps)

### 1. Push changes to GitHub
```bash
git add .
git commit -m "Fix Vercel deployment - add WSGI handler"
git push origin main
```

### 2. Redeploy on Vercel
- Go to your Vercel dashboard: https://vercel.com/dashboard
- Click on your phishlab project
- Click "Redeploy" button
- Wait 3-5 minutes for the build

### 3. Check the logs
- If it still fails, click "View Function Logs"
- Look for error messages

---

## 🗄️ Important: Database Issue

**⚠️ SQLite doesn't work on Vercel** (ephemeral filesystem)

Your app currently uses SQLite, which loses data on every deployment. For Vercel, you need to:

### Option A: Use Render.com Instead (Keeps SQLite)
This is simpler! Go back to Render.com with your app.

### Option B: Keep Vercel + Switch to PostgreSQL
1. Create a free PostgreSQL database:
   - **Railway.app** - https://railway.app (FREE tier with connection string)
   - **Neon** - https://neon.tech (FREE PostgreSQL)

2. Get your database URL (looks like):
   ```
   postgresql://username:password@host.neon.tech/dbname
   ```

3. In Vercel Dashboard:
   - Go to Settings → Environment Variables
   - Add: `DATABASE_URL` = your PostgreSQL connection string
   - Save and Redeploy

---

## 📋 Checklist
- [ ] Push code to GitHub with new files
- [ ] Click "Redeploy" on Vercel dashboard
- [ ] Wait for build to succeed
- [ ] Check browser - should no longer see 500 error
- [ ] If using SQLite: Switch to PostgreSQL (see steps above)

---

## 🆘 Still Getting 500 Error?
1. Go to Vercel dashboard → Your project → Function Logs
2. Copy the error message
3. Common fixes:
   - Missing environment variables → Set them in Settings
   - Database connection error → Check DATABASE_URL format
   - Missing Python packages → They auto-install from requirements.txt

Need help? Let me know the exact error from the Function Logs!
