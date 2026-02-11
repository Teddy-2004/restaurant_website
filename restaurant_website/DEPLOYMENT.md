# 🚀 Deployment Guide

This guide covers deploying the restaurant website to various platforms.

## Table of Contents
- [Railway Deployment](#railway-deployment)
- [Render Deployment](#render-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Traditional VPS](#traditional-vps-ubuntu)
- [Docker Deployment](#docker-deployment)

---

## Railway Deployment

Railway is recommended for its simplicity and PostgreSQL integration.

### Steps:

1. **Prepare the project**
   ```bash
   # Ensure you have Procfile and requirements.txt
   pip freeze > requirements.txt
   ```

2. **Create Railway account**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Deploy**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Flask and deploys

4. **Add PostgreSQL**
   - In your project, click "New"
   - Select "Database" → "PostgreSQL"
   - Railway automatically sets DATABASE_URL

5. **Set Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

6. **Initialize Database**
   ```bash
   # Connect via Railway CLI
   railway run flask db upgrade
   railway run python create_admin.py
   ```

7. **Access your app**
   - Railway provides a `.railway.app` domain
   - Or connect custom domain in settings

---

## Render Deployment

### Steps:

1. **Create Render account**
   - Visit [render.com](https://render.com)

2. **Create Web Service**
   - New → Web Service
   - Connect GitHub repository
   - Configure:
     - **Name**: restaurant-website
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn run:app`

3. **Add PostgreSQL Database**
   - New → PostgreSQL
   - Copy the Internal Database URL

4. **Environment Variables**
   ```
   DATABASE_URL=<from PostgreSQL>
   SECRET_KEY=<generate-random-key>
   FLASK_ENV=production
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. **Deploy**
   - Render auto-deploys on git push
   - Access via `your-app.onrender.com`

---

## Heroku Deployment

### Steps:

1. **Install Heroku CLI**
   ```bash
   # On Mac
   brew tap heroku/brew && brew install heroku
   
   # On Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create restaurant-website-app
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set MAIL_SERVER=smtp.gmail.com
   heroku config:set MAIL_USERNAME=your-email@gmail.com
   heroku config:set MAIL_PASSWORD=your-password
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push heroku main
   ```

6. **Initialize Database**
   ```bash
   heroku run flask db upgrade
   heroku run python create_admin.py
   ```

7. **Open App**
   ```bash
   heroku open
   ```

---

## Traditional VPS (Ubuntu)

### Prerequisites
- Ubuntu 20.04+ server
- Root or sudo access
- Domain name (optional)

### Steps:

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Dependencies**
   ```bash
   sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y
   ```

3. **Setup PostgreSQL**
   ```bash
   sudo -u postgres psql
   
   CREATE DATABASE restaurant_db;
   CREATE USER restaurant_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE restaurant_db TO restaurant_user;
   \q
   ```

4. **Clone and Setup Application**
   ```bash
   cd /var/www
   sudo git clone your-repo-url restaurant
   cd restaurant
   sudo chown -R $USER:$USER /var/www/restaurant
   
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   # Edit with your production settings
   ```

6. **Initialize Database**
   ```bash
   flask db upgrade
   python create_admin.py
   ```

7. **Setup Gunicorn Service**
   ```bash
   sudo nano /etc/systemd/system/restaurant.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Restaurant Website
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/restaurant
   Environment="PATH=/var/www/restaurant/venv/bin"
   ExecStart=/var/www/restaurant/venv/bin/gunicorn --workers 3 --bind unix:restaurant.sock -m 007 run:app

   [Install]
   WantedBy=multi-user.target
   ```
   
   Enable and start:
   ```bash
   sudo systemctl start restaurant
   sudo systemctl enable restaurant
   ```

8. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/restaurant
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/restaurant/restaurant.sock;
       }

       location /static {
           alias /var/www/restaurant/app/static;
       }

       location /uploads {
           alias /var/www/restaurant/app/static/uploads;
       }
   }
   ```
   
   Enable site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Setup SSL (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

10. **Setup Firewall**
    ```bash
    sudo ufw allow 'Nginx Full'
    sudo ufw enable
    ```

---

## Docker Deployment

### Create Dockerfile:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]
```

### Create docker-compose.yml:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/restaurant
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./app/static/uploads:/app/app/static/uploads

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=restaurant
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Deploy:

```bash
docker-compose up -d
docker-compose exec web flask db upgrade
docker-compose exec web python create_admin.py
```

---

## Post-Deployment Checklist

- [ ] Change default admin password
- [ ] Configure email settings
- [ ] Set up backups
- [ ] Configure monitoring (New Relic, Datadog)
- [ ] Set up error tracking (Sentry)
- [ ] Configure CDN for static files (Cloudflare)
- [ ] Add Google Analytics
- [ ] Set up SSL/HTTPS
- [ ] Configure domain and DNS
- [ ] Test all functionality
- [ ] Create sample content

---

## Troubleshooting

### Database Connection Issues
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

### Static Files Not Loading
```bash
# Ensure correct permissions
chmod -R 755 app/static

# Collect static files if using CDN
flask collect-static
```

### Application Won't Start
```bash
# Check logs
heroku logs --tail  # For Heroku
railway logs        # For Railway
sudo journalctl -u restaurant -f  # For systemd
```

### Email Not Sending
- Verify SMTP credentials
- Enable "Less secure apps" for Gmail
- Use app-specific password
- Check firewall rules for port 587

---

## Performance Optimization

1. **Enable Caching**
   ```python
   # Add Flask-Caching
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

2. **Use CDN for Static Files**
   - CloudFlare
   - AWS CloudFront
   - Fastly

3. **Database Optimization**
   ```python
   # Add indexes to frequently queried fields
   # Use connection pooling
   ```

4. **Enable Gzip Compression**
   ```nginx
   gzip on;
   gzip_types text/plain text/css application/json application/javascript;
   ```

---

## Monitoring & Maintenance

- Set up uptime monitoring (UptimeRobot, Pingdom)
- Configure automated backups
- Monitor application errors
- Review logs regularly
- Keep dependencies updated
- Security patches and updates

---

**Need Help?** Open an issue on GitHub or contact support.
