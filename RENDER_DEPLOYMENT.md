# 🚀 Deploy to Render - Complete Guide

Render is an excellent platform! Easy, affordable, and perfect for this API.

## 🎯 Why Render?

✅ **Free tier available** - Start with no cost
✅ **Docker support** - Works perfectly with our setup
✅ **Auto-deploys** - Deploy on git push
✅ **Auto-scaling** - Handles traffic spikes
✅ **PostgreSQL included** - If you need database later
✅ **Easy setup** - 10 minutes total
✅ **Custom domains** - Free SSL certificate
✅ **$7/month paid** - Very affordable

---

## 📋 REQUIREMENTS

Before starting, have ready:
- [ ] GitHub account (https://github.com)
- [ ] Render account (https://render.com)
- [ ] Your code pushed to GitHub
- [ ] `requirements.txt` (we have this ✓)
- [ ] `Dockerfile` (we have this ✓)

---

## 🔧 STEP-BY-STEP SETUP (10 minutes)

### **STEP 1: Create GitHub Repository**

**1.1 Go to GitHub**
```
https://github.com/new
```

**1.2 Create repository**
- Name: `yolo-detection-api`
- Description: "YOLO Object Detection API with live streaming"
- Visibility: Public (or private if you want)
- Click "Create repository"

**1.3 Push your code to GitHub**

In your `train` folder:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial YOLO Detection API"

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/yolo-detection-api.git

# Push
git branch -M main
git push -u origin main
```

**Verify:** Visit `https://github.com/YOUR_USERNAME/yolo-detection-api`
You should see all your files there ✓

---

### **STEP 2: Create Render Account**

**2.1 Go to Render**
```
https://render.com
```

**2.2 Sign up**
- Click "Sign Up"
- Use GitHub (easiest option)
- Authorize Render to access GitHub
- Done!

---

### **STEP 3: Create Web Service on Render**

**3.1 Dashboard**
After login, go to: Dashboard

**3.2 Create new service**
- Click "+ New"
- Select "Web Service"

**3.3 Connect GitHub**
- Click "Connect account" (if not done)
- Select your `yolo-detection-api` repository
- Click "Connect"

**3.4 Configure service**

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `yolo-detection-api` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Docker` |
| **Build Command** | (leave empty) |
| **Start Command** | (leave empty) |

**3.5 Select Plan**

- **Free** - Good for testing
- **Starter** - $7/month (recommended)

*Note: Free tier sleeps after 15 min inactivity*

**3.6 Create service**
- Scroll down
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)

---

### **STEP 4: Configure Environment Variables (Optional)**

**4.1 Go to Environment**
- In your service dashboard
- Click "Environment"

**4.2 Add variables** (optional, default values are fine):

```
MODEL_PATH=/app/weights/final.pt
CONFIDENCE_THRESHOLD=0.5
MAX_DETECTIONS=100
```

---

### **STEP 5: Wait for Deployment**

**5.1 Monitor deployment**
- Go to "Logs" tab
- Watch the build process
- Should see: `Application is live at: https://yolo-detection-api-xxxxx.onrender.com`

**5.2 Once deployed**
Visit your API:
```
https://yolo-detection-api-xxxxx.onrender.com/docs
```

**You should see the interactive API documentation!** ✓

---

## ✅ VERIFY DEPLOYMENT

### **Test 1: Health Check**
```bash
curl https://yolo-detection-api-xxxxx.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes": 7,
  "timestamp": "2025-01-12T10:30:00"
}
```

### **Test 2: API Docs**
Open in browser:
```
https://yolo-detection-api-xxxxx.onrender.com/docs
```

You should see Swagger API documentation

### **Test 3: Detect Image**

Using the Swagger UI:
1. Click on `POST /detect/image`
2. Click "Try it out"
3. Upload an image
4. Click "Execute"
5. See detection results!

---

## 🔄 AUTO-DEPLOYMENT

**Great news:** Your API auto-deploys on every git push!

### **To update your API:**

```bash
# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Update detection threshold"

# Push
git push origin main

# Render automatically redeploys!
# Check status: https://dashboard.render.com
```

---

## 📊 RENDER DASHBOARD

Your service dashboard shows:

- **Logs** - See what's happening
- **Metrics** - CPU, Memory, Request count
- **Environment** - Set variables
- **Settings** - Configure service
- **Deploys** - Deployment history

---

## 🌐 CUSTOM DOMAIN (Optional)

**Add your own domain:**

1. Go to "Settings"
2. Scroll to "Custom Domain"
3. Enter your domain: `api.yourdomain.com`
4. Render provides SSL certificate (free!)
5. Point your domain to Render (instructions provided)

---

## 💰 PRICING

| Plan | Cost | Limits |
|------|------|--------|
| **Free** | $0 | Sleeps after 15 min |
| **Starter** | $7/month | 2.5GB RAM, always on |
| **Standard** | $25/month | 4GB RAM, more features |
| **Pro** | $50+/month | High performance |

**Recommended:** Start with Free, upgrade to Starter ($7/mo) if needed

---

## 🚨 IMPORTANT NOTES

### Model Size
⚠️ Your model (`final.pt`) is ~100MB

Render has:
- Free: 10GB deploy size limit ✓
- Starter: 50GB ✓

No problem!

### Memory
- Free tier: 512MB (may be tight)
- Starter: 2.5GB (recommended)

If you get "Out of Memory" errors, upgrade to Starter tier.

### First Request Timeout
On free tier, first request may take 30+ seconds (waking up from sleep).

---

## 🐛 TROUBLESHOOTING

### Issue: "Build failed"

**Solution:**
```bash
# Check requirements.txt
cat requirements.txt

# Ensure all dependencies are listed
# Push fix to GitHub
git push origin main
# Render auto-redeploys
```

### Issue: "Out of memory"

**Solution:**
1. Upgrade from Free to Starter tier
2. Or reduce model batch size in `api.py`

### Issue: "Service takes too long to start"

**Solution:**
1. This is normal on free tier (spinning up)
2. Upgrade to Starter for instant deployment
3. First request may take 30+ seconds

### Issue: "Can't upload large files"

**Solution:**
In `api.py`, increase upload limit:
```python
app = FastAPI()
# Add after initialization:
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 📱 USING YOUR API

### From Python

```python
import requests

API_URL = "https://yolo-detection-api-xxxxx.onrender.com"

# Image detection
with open("photo.jpg", "rb") as f:
    response = requests.post(
        f"{API_URL}/detect/image",
        files={"file": f}
    )
    result = response.json()
    print(f"Found {result['num_detections']} objects")
```

### From JavaScript

```javascript
const API_URL = "https://yolo-detection-api-xxxxx.onrender.com";

async function detectImage(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_URL}/detect/image`, {
        method: 'POST',
        body: formData
    });
    
    const result = await response.json();
    console.log(`Found ${result.num_detections} objects`);
}
```

### From cURL

```bash
curl -X POST https://yolo-detection-api-xxxxx.onrender.com/detect/image \
  -F "file=@image.jpg"
```

---

## 🎯 COMPLETE RENDER SETUP CHECKLIST

- [ ] GitHub account created
- [ ] Code pushed to GitHub repository
- [ ] Render account created
- [ ] Web Service created from GitHub repo
- [ ] Docker runtime selected
- [ ] Deployment completed (check logs)
- [ ] API docs accessible
- [ ] Health check works
- [ ] Image detection tested
- [ ] (Optional) Custom domain configured

---

## 🚀 NEXT STEPS

### Immediate (Now)
1. ✅ Push code to GitHub
2. ✅ Create Render service
3. ✅ Test API endpoints
4. ✅ Share your URL!

### Soon (This Week)
1. Add custom domain
2. Set up monitoring
3. Configure alerts

### Later (This Month)
1. Upgrade tier if needed
2. Add authentication
3. Implement rate limiting

---

## 📞 SUPPORT & RESOURCES

- **Render Docs:** https://render.com/docs
- **Your API Docs:** https://yolo-detection-api-xxxxx.onrender.com/docs
- **GitHub:** https://github.com/your-username/yolo-detection-api
- **Status:** https://status.render.com

---

## 🎉 YOUR DEPLOYED API

Once deployed on Render:

✅ **URL:** `https://yolo-detection-api-xxxxx.onrender.com`
✅ **API Docs:** `https://yolo-detection-api-xxxxx.onrender.com/docs`
✅ **Endpoints:**
- POST `/detect/image` - Image detection
- POST `/detect/video` - Video processing
- WS `/ws/webcam` - Live webcam
- GET `/health` - Health check

✅ **Auto-deploys:** On every git push
✅ **HTTPS:** Free SSL certificate
✅ **Monitoring:** Available in dashboard

---

## 💡 TIPS

1. **Keep API logs clean** - Monitor in dashboard
2. **Set up alerts** - Render can email you on errors
3. **Monitor usage** - Check metrics regularly
4. **Upgrade to Starter** - If you plan to use daily
5. **Use custom domain** - Makes it professional

---

## 📝 GITHUB SETUP QUICK REFERENCE

```bash
# One-time setup
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/yolo-detection-api.git
git branch -M main
git push -u origin main

# After this, just:
git add .
git commit -m "Your message"
git push origin main
# Render auto-deploys!
```

---

## 🌟 FINAL CHECKLIST

Before you deploy:

- [ ] `requirements.txt` exists
- [ ] `Dockerfile` exists
- [ ] `backend/weights/final.pt` exists
- [ ] `backend/api.py` exists
- [ ] All pushed to GitHub
- [ ] Render account created
- [ ] Web Service configured

Everything? **Deploy now!** 🚀

---

**Ready to deploy? Start with Step 1: Create GitHub Repository**

Questions? Check the DEPLOYMENT_GUIDE.md for more details!
