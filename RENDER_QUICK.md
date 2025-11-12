# 🎯 RENDER DEPLOYMENT - QUICK REFERENCE

## ⚡ 10-MINUTE DEPLOYMENT

### Step 1️⃣: GitHub (5 minutes)

```bash
# In your train folder:
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/yolo-detection-api.git
git branch -M main
git push -u origin main
```

### Step 2️⃣: Render (5 minutes)

1. Go to: https://render.com
2. Sign up with GitHub
3. Click "+ New" → "Web Service"
4. Select your repository
5. Fill in:
   - **Name:** `yolo-detection-api`
   - **Runtime:** Docker
   - **Plan:** Free (or Starter $7/mo)
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment

### Step 3️⃣: Done! 🎉

Your API is live at:
```
https://yolo-detection-api-xxxxx.onrender.com/docs
```

---

## ✅ VERIFY IT WORKS

### Browser Test
```
https://yolo-detection-api-xxxxx.onrender.com/docs
```
Should show interactive API docs ✓

### CLI Test
```bash
curl https://yolo-detection-api-xxxxx.onrender.com/health
```

Should return:
```json
{"status": "healthy", "model_loaded": true}
```

---

## 🔄 AUTO-UPDATE

After first deployment, just push to GitHub:

```bash
# Make changes
# ... edit code ...

# Push
git add .
git commit -m "Update message"
git push origin main

# Render automatically redeploys! ✓
```

---

## 📊 RENDER DASHBOARD

Monitor your API:
```
https://dashboard.render.com
→ Click your service
→ See Logs, Metrics, Settings
```

---

## 💰 PRICING

| Plan | Cost | Best For |
|------|------|----------|
| Free | $0 | Testing |
| Starter | $7/mo | Production ⭐ |

Free tier sleeps after 15 min. Upgrade to Starter if using daily.

---

## 🚀 AFTER DEPLOYMENT

### Share Your API
```
API URL: https://yolo-detection-api-xxxxx.onrender.com
Docs: https://yolo-detection-api-xxxxx.onrender.com/docs
```

### Add Custom Domain (Optional)
1. Go to Service Settings
2. Add your domain: `api.yourdomain.com`
3. Follow Render instructions
4. Free SSL certificate included!

### Monitor Performance
1. Go to Metrics tab
2. Check CPU, Memory, Requests
3. Upgrade tier if needed

---

## ⚠️ COMMON ISSUES

### "Out of Memory"
→ Upgrade to Starter tier ($7/mo)

### "Build failed"
→ Check Logs tab, fix error, push to GitHub again

### "First request slow"
→ Normal on free tier (waking up from sleep)

### "File too large"
→ Model is 100MB, Render supports up to 10GB

---

## 📱 USE YOUR API

### Python
```python
import requests

API = "https://yolo-detection-api-xxxxx.onrender.com"
with open("photo.jpg", "rb") as f:
    r = requests.post(f"{API}/detect/image", files={"file": f})
    print(r.json())
```

### JavaScript
```javascript
const API = "https://yolo-detection-api-xxxxx.onrender.com";
const formData = new FormData();
formData.append('file', file);
const r = await fetch(`${API}/detect/image`, {
    method: 'POST',
    body: formData
});
const data = await r.json();
```

### cURL
```bash
curl -X POST https://yolo-detection-api-xxxxx.onrender.com/detect/image \
  -F "file=@image.jpg"
```

---

## 📋 BEFORE YOU DEPLOY

Checklist:
- [ ] GitHub account (https://github.com)
- [ ] Render account (https://render.com)
- [ ] Code pushed to GitHub
- [ ] `requirements.txt` exists
- [ ] `Dockerfile` exists
- [ ] Model file: `backend/weights/final.pt` exists

All set? Deploy now! 🚀

---

## 🎯 ENDPOINTS

Once deployed:

```
GET  https://yolo-detection-api-xxxxx.onrender.com/health
GET  https://yolo-detection-api-xxxxx.onrender.com/docs
POST https://yolo-detection-api-xxxxx.onrender.com/detect/image
POST https://yolo-detection-api-xxxxx.onrender.com/detect/video
WS   wss://yolo-detection-api-xxxxx.onrender.com/ws/webcam
```

---

## 💡 TIPS

1. **Free tier limits**
   - Sleeps after 15 min idle
   - 512MB RAM
   - Good for testing

2. **Starter tier ($7/mo)**
   - Always on
   - 2.5GB RAM
   - Recommended for production

3. **First request**
   - May take 30+ sec on free tier (waking up)
   - Instant on Starter tier

4. **Updates**
   - Auto-deploy on `git push`
   - No manual redeploy needed

---

## 🎉 SUCCESS!

Once you see your API docs loading at:
```
https://yolo-detection-api-xxxxx.onrender.com/docs
```

You're ready to:
- ✅ Upload images
- ✅ Detect objects
- ✅ Process videos
- ✅ Stream webcam
- ✅ Share with others

Congratulations! Your API is live! 🚀

---

**Need more details? See RENDER_DEPLOYMENT.md**
