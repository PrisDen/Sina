# 🚀 Sina Deployment Guide

Complete guide for deploying Sina - The Disciplined Mentor in various environments.

## 📋 Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- Network access (for cloud deployments)

## 🏠 Local Development

### Quick Start
```bash
git clone https://github.com/PrisDen/Sina.git
cd Sina
pip install -r requirements.txt
python3 deploy.py
```

Select option 1 for local development or option 2 for network access.

## 🌐 Production Deployment Options

### Option 1: Local Network (Home/Office)

**Best for:** Personal use, small teams, home networks

```bash
# Clone and setup
git clone https://github.com/PrisDen/Sina.git
cd Sina
pip install -r requirements.txt

# Run with production script
python3 deploy.py
# Select option 2 for network access

# Or run directly
python3 app.py
```

**Access:** `http://YOUR_IP:5001` from any device on your network

### Option 2: Cloud Deployment - Heroku (Free)

**Best for:** Easy cloud deployment, no server management

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login and create app
heroku login
heroku create your-sina-app

# Deploy
git push heroku master

# Open your app
heroku open
```

**Access:** `https://your-sina-app.herokuapp.com`

### Option 3: Cloud Deployment - Railway

**Best for:** Modern cloud platform, automatic deployments

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Select the Sina repository
4. Railway will automatically deploy
5. Get your deployment URL

**Access:** `https://your-app.railway.app`

### Option 4: DigitalOcean App Platform

**Best for:** Scalable cloud deployment

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub
3. Select Sina repository
4. Choose Python app type
5. Deploy automatically

**Access:** `https://your-app.ondigitalocean.app`

### Option 5: Self-Hosted VPS (Advanced)

**Best for:** Full control, custom domains, high performance

#### Ubuntu/Debian Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create user for Sina
sudo useradd -m -s /bin/bash sina
sudo su - sina

# Clone and setup
git clone https://github.com/PrisDen/Sina.git
cd Sina
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Test the application
python3 app.py
```

#### Production WSGI Setup with Gunicorn

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn

# Test gunicorn
gunicorn --bind 0.0.0.0:5001 wsgi:app

# Create systemd service
sudo nano /etc/systemd/system/sina.service
```

**Systemd Service File:**
```ini
[Unit]
Description=Sina - The Disciplined Mentor
After=network.target

[Service]
User=sina
Group=sina
WorkingDirectory=/home/sina/Sina
Environment=PATH=/home/sina/Sina/venv/bin
Environment=FLASK_ENV=production
Environment=SECRET_KEY=your-secret-key-here
ExecStart=/home/sina/Sina/venv/bin/gunicorn --bind 0.0.0.0:5001 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable sina
sudo systemctl start sina
sudo systemctl status sina
```

#### Nginx Reverse Proxy

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/sina
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/sina/Sina/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/sina /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### SSL with Let's Encrypt (Optional)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔧 Environment Variables

### Required for Production

```bash
export FLASK_ENV=production
export SECRET_KEY=your-very-secure-secret-key-here
export PORT=5001
```

### Optional Configuration

```bash
export DATABASE_URL=sqlite:///instance/sina.db
export LOG_LEVEL=INFO
export MAX_CONTENT_LENGTH=16777216  # 16MB
```

## 📊 Monitoring and Maintenance

### Health Check Endpoint

Sina includes a health check endpoint:
```
GET /test
```

Returns:
```json
{
  "status": "success",
  "message": "Sina app is running correctly!",
  "timestamp": "2025-05-26T10:30:00"
}
```

### Log Monitoring

```bash
# View application logs
sudo journalctl -u sina -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Database Backup

```bash
# Backup SQLite database
cp instance/sina.db backups/sina_$(date +%Y%m%d_%H%M%S).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/home/sina/backups"
mkdir -p $BACKUP_DIR
cp /home/sina/Sina/instance/sina.db $BACKUP_DIR/sina_$(date +%Y%m%d_%H%M%S).db
find $BACKUP_DIR -name "sina_*.db" -mtime +30 -delete
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Change default secret key
- [ ] Use HTTPS in production
- [ ] Regular database backups
- [ ] Monitor application logs
- [ ] Keep dependencies updated
- [ ] Use firewall rules
- [ ] Regular security updates

### Firewall Setup (UFW)

```bash
# Basic firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   sudo lsof -i :5001
   sudo kill -9 PID
   ```

2. **Permission denied**
   ```bash
   sudo chown -R sina:sina /home/sina/Sina
   chmod +x deploy.py
   ```

3. **Database locked**
   ```bash
   sudo systemctl stop sina
   rm instance/sina.db
   sudo systemctl start sina
   ```

4. **Nginx 502 Bad Gateway**
   ```bash
   sudo systemctl status sina
   sudo systemctl restart sina
   sudo systemctl restart nginx
   ```

### Performance Optimization

```bash
# Increase Gunicorn workers
gunicorn --workers 4 --bind 0.0.0.0:5001 wsgi:app

# Enable Nginx gzip compression
# Add to nginx.conf:
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

## 📱 Mobile Access

Sina is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Mobile phones (iOS/Android)
- ✅ Tablets
- ✅ Smart TVs with browsers

## 🎯 Success Metrics

After deployment, verify:
- [ ] Application loads correctly
- [ ] User registration works
- [ ] Task creation/completion functions
- [ ] Timer system operates
- [ ] Journal saves entries
- [ ] Analytics display data
- [ ] Deadline notifications appear
- [ ] Mobile responsiveness

## 🆘 Support

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/PrisDen/Sina/issues)
2. Review application logs
3. Verify all dependencies are installed
4. Ensure proper file permissions
5. Check network connectivity

---

**🎉 Congratulations! Sina is now deployed and ready to help build unshakeable discipline!** 