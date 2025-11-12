# 🚀 Deployment Guide - Choose Your Best Option

Your YOLO Detection API is built and running. Now let's deploy it!

## 📊 Deployment Options Comparison

| Option | Ease | Cost | Scalability | Best For | Setup Time |
|--------|------|------|-------------|----------|-----------|
| **Local** | ⭐⭐⭐⭐⭐ | Free | Single machine | Development, Testing | 5 min |
| **Docker Local** | ⭐⭐⭐⭐ | Free | Single machine | Production local | 10 min |
| **AWS EC2** | ⭐⭐⭐ | $$ | Highly scalable | Production web | 30 min |
| **Google Cloud Run** | ⭐⭐⭐⭐ | $ | Auto-scaling | Serverless, API only | 20 min |
| **Heroku** | ⭐⭐⭐⭐⭐ | $ | Limited | Quick prototyping | 15 min |
| **DigitalOcean** | ⭐⭐⭐⭐ | $ | Good | Balanced option | 20 min |
| **Docker Hub** | ⭐⭐⭐⭐ | Free/$ | Custom | Image distribution | 25 min |

---

## 🎯 RECOMMENDED: Docker (Most Practical)

### Why Docker?
✅ Works anywhere
✅ Easy to update
✅ Consistent environment
✅ Great for production
✅ Easy to scale

### Quick Docker Deploy

**Step 1: Build Docker Image**
```bash
cd train/backend
docker build -t yolo-detection-api:latest .
```

**Step 2: Run Container**
```bash
docker run -p 8000:8000 \
  -v $(pwd)/results:/app/results \
  yolo-detection-api:latest
```

**Step 3: Access**
```
http://localhost:8000/docs
```

### Or Use Docker Compose (Easiest!)

**One Command:**
```bash
cd train
docker-compose up
```

**Access:**
- API: http://localhost:8000
- Dashboard: http://localhost:3000

---

## 🥇 BEST FOR BEGINNERS: Heroku

### Why Heroku?
✅ Easiest setup
✅ No infrastructure knowledge needed
✅ Automatic updates
✅ Free tier available
✅ Works immediately

### Deploy to Heroku (15 minutes)

**Step 1: Create Procfile**
```bash
cd train/backend
# Create file: Procfile
echo "web: uvicorn api:app --host 0.0.0.0 --port \$PORT" > Procfile
```

**Step 2: Create Heroku Account**
Visit: https://www.heroku.com/

**Step 3: Install Heroku CLI**
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
# Or with Chocolatey:
choco install heroku-cli
```

**Step 4: Login & Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Step 5: Access**
```
https://your-app-name.herokuapp.com/docs
```

### Heroku Cost
- Free tier: Limited (sleeps after 30 min inactivity)
- Paid: $7+/month

---

## 🌐 BEST FOR PRODUCTION: AWS EC2

### Why AWS?
✅ Full control
✅ Excellent scalability
✅ 24/7 uptime
✅ Advanced features
✅ Industry standard

### Deploy to AWS EC2 (30 minutes)

**Step 1: Launch EC2 Instance**
1. Go to: https://aws.amazon.com/
2. Create account
3. Launch instance:
   - Image: Ubuntu 22.04
   - Instance: t3.medium (1 GB RAM min)
   - Security: Allow ports 80, 443, 8000
   - Storage: 20 GB

**Step 2: SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

**Step 3: Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Clone your repo
git clone your-repo-url
cd train

# Start with Docker Compose
docker-compose up -d
```

**Step 4: Setup Domain (Optional)**
- Buy domain on Route53, GoDaddy, etc.
- Point to EC2 elastic IP
- Use Let's Encrypt for HTTPS

**Step 5: Access**
```
http://your-domain.com/docs
```

### AWS Cost
- t3.medium: ~$30/month
- Data transfer: ~$0.09/GB

---

## ☁️ BEST FOR SERVERLESS: Google Cloud Run

### Why Cloud Run?
✅ Pay only for usage
✅ Auto-scales to zero
✅ Simple deployment
✅ Free tier: 2M requests/month
✅ No infrastructure management

### Deploy to Google Cloud Run (20 minutes)

**Step 1: Create Google Cloud Account**
Visit: https://cloud.google.com/

**Step 2: Install Google Cloud SDK**
```bash
# Download from: https://cloud.google.com/sdk/docs/install
# Or with Chocolatey:
choco install google-cloud-sdk
```

**Step 3: Authenticate**
```bash
gcloud auth login
gcloud config set project your-project-id
```

**Step 4: Build & Deploy**
```bash
cd train/backend

# Build image
gcloud builds submit --tag gcr.io/your-project/yolo-api

# Deploy to Cloud Run
gcloud run deploy yolo-api \
  --image gcr.io/your-project/yolo-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --timeout 900
```

**Step 5: Access**
```
https://yolo-api-xxxxx.run.app/docs
```

### Cloud Run Cost
- Free: 2M requests/month
- Usage: $0.00002400 per request
- Typical: $5-20/month

---

## 💻 BEST VALUE: DigitalOcean

### Why DigitalOcean?
✅ Easy to use
✅ Affordable
✅ Docker-native
✅ Good documentation
✅ $5-20/month

### Deploy to DigitalOcean (20 minutes)

**Step 1: Create DigitalOcean Account**
Visit: https://www.digitalocean.com/

**Step 2: Create Droplet**
1. Click "Create" → "Droplets"
2. Choose:
   - Image: Docker (pre-installed)
   - Size: $6/month (2GB RAM)
   - Region: Closest to you
3. Create

**Step 3: SSH into Droplet**
```bash
ssh root@your-droplet-ip
```

**Step 4: Deploy**
```bash
# Clone repo
git clone your-repo-url
cd train

# Start with Docker Compose
docker-compose up -d
```

**Step 5: Setup Firewall**
```bash
# Allow ports
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 8000
ufw enable
```

**Step 6: Access**
```
http://your-droplet-ip:8000/docs
```

### DigitalOcean Cost
- Droplet: $6/month
- Domain: $3-12/year

---

## 📦 BEST FOR CI/CD: GitHub Actions + Docker Hub

### Why GitHub Actions?
✅ Free
✅ Automated testing
✅ Auto-deploy on push
✅ Built-in Docker Hub integration
✅ Professional workflow

### Setup GitHub Actions (30 minutes)

**Step 1: Create GitHub Repo**
```bash
cd train
git init
git add .
git commit -m "Initial commit"
git remote add origin your-repo-url
git push -u origin main
```

**Step 2: Create GitHub Secrets**
1. Go to: Settings → Secrets
2. Add:
   - DOCKER_USERNAME
   - DOCKER_PASSWORD
   - DOCKER_REGISTRY_URL

**Step 3: Create Workflow File**
```bash
mkdir -p .github/workflows
# Create .github/workflows/deploy.yml:
```

**deploy.yml Content:**
```yaml
name: Deploy to Docker Hub

on:
  push:
    branches: [ main ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      
      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: ./backend
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/yolo-api:latest
```

**Step 4: Push & Auto-Deploy**
```bash
git push origin main
# Automatically builds and pushes to Docker Hub!
```

---

## 🎯 DECISION MATRIX - Choose Based on Your Needs

### I just want to test it locally
→ **Docker Compose** (5 min)
```bash
cd train && docker-compose up
```

### I want quick & easy deployment
→ **Heroku** (15 min, $7/month)
```bash
git push heroku main
```

### I want best value
→ **DigitalOcean** (20 min, $6/month)
```bash
SSH in, docker-compose up
```

### I need production & scalability
→ **AWS EC2** (30 min, $30/month)
```bash
EC2 + Docker Compose
```

### I want serverless & pay-per-use
→ **Google Cloud Run** (20 min, $5-20/month)
```bash
gcloud run deploy
```

### I want fully automated CI/CD
→ **GitHub Actions + Cloud** (30 min)
```bash
Auto-deploy on push
```

---

## 🚀 STEP-BY-STEP FOR EACH OPTION

### Option 1: Docker Local (Recommended to Start)

```bash
# Build image
cd train/backend
docker build -t yolo-api:latest .

# Run
docker run -p 8000:8000 \
  -v ./results:/app/results \
  yolo-api:latest

# Access: http://localhost:8000/docs
```

### Option 2: Docker Compose (Easiest for Full Stack)

```bash
cd train
docker-compose up

# Access:
# API: http://localhost:8000/docs
# Dashboard: http://localhost:3000
```

### Option 3: Heroku (Quickest Cloud)

```bash
# Prerequisites
heroku login
heroku create your-app-name

# Deploy
git push heroku main

# Access: https://your-app-name.herokuapp.com/docs
```

### Option 4: AWS EC2 (Most Control)

```bash
# Launch instance, SSH in, then:
sudo apt update
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ubuntu
git clone your-repo
cd train
docker-compose up -d

# Access: http://your-instance-ip:8000/docs
```

### Option 5: Google Cloud Run (Best for Serverless)

```bash
gcloud run deploy yolo-api \
  --source train/backend \
  --platform managed \
  --memory 2Gi

# Access: https://yolo-api-xxxxx.run.app/docs
```

---

## 📋 Pre-Deployment Checklist

- [ ] API runs locally: `python api.py`
- [ ] Health check passes: `curl http://localhost:8000/health`
- [ ] Image detection works
- [ ] Video processing works
- [ ] Docker image builds: `docker build -t yolo-api .`
- [ ] requirements.txt is updated
- [ ] Dockerfile is correct
- [ ] All secrets are configured
- [ ] Ports are accessible

---

## 🔒 Security for Production

1. **Environment Variables**
   ```bash
   # Don't hardcode config!
   export MODEL_PATH=/app/weights/final.pt
   export CONFIDENCE_THRESHOLD=0.5
   ```

2. **HTTPS/SSL**
   ```bash
   # Use Let's Encrypt (free)
   sudo apt install certbot
   sudo certbot certonly --standalone -d your-domain.com
   ```

3. **API Authentication** (Optional)
   - Add API keys
   - Implement JWT tokens
   - Rate limiting

4. **File Permissions**
   ```bash
   # Secure file access
   chmod 755 weights/
   chmod 644 weights/final.pt
   ```

---

## 📊 RECOMMENDED DEPLOYMENT PATH

### Phase 1: Development (Local)
```
Start here → Run locally → Test features
python api.py
```

### Phase 2: Staging (Docker Local)
```
Package app → Test in container
docker-compose up
```

### Phase 3: Production (Choose One)
```
Option A: Heroku (Easiest, $7/mo)
Option B: Docker + AWS (Most control, $30/mo)
Option C: Cloud Run (Cheapest, $0-20/mo)
```

---

## 🆘 Troubleshooting Deployment

### Docker won't build
```bash
# Check Dockerfile
docker build -t yolo-api:latest . --verbose
```

### Port already in use
```bash
# Find process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Out of memory
```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory: 4GB
```

### API can't access model
```bash
# Check volume mount
docker run -v ./weights:/app/weights ...
```

---

## 💡 My Recommendation

**For Most Users:** Docker Compose on DigitalOcean
- Simple setup (20 min)
- Affordable ($6/month)
- Professional results
- Easy to manage

**For Quick Testing:** Local Docker
```bash
docker-compose up
```

**For Production at Scale:** AWS EC2 + CI/CD
```bash
Automated deployments, full control
```

---

## 📞 Quick Links

- [Heroku Deployment](https://devcenter.heroku.com/articles/getting-started-with-python)
- [AWS EC2 Guide](https://docs.aws.amazon.com/ec2/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [DigitalOcean Docs](https://docs.digitalocean.com/)
- [Docker Documentation](https://docs.docker.com/)

---

**Which deployment option interests you most? I can walk you through the setup!**
