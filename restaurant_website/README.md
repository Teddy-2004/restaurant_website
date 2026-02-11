# 🍽️ Mediterranean Restaurant Website

A modern, full-stack restaurant website built with Flask and Bootstrap 5.

## 🌟 Features

- **Responsive Design**: Mobile-first Bootstrap 5 implementation
- **Reservation System**: Real-time table booking with email confirmations
- **Interactive Menu**: Searchable, filterable menu with categories
- **Admin Dashboard**: Complete CMS for managing all content
- **Gallery**: Lazy-loading image gallery with lightbox
- **Reviews**: Customer testimonials management
- **Events & Promotions**: Dynamic events calendar
- **Contact Form**: Validated forms with email integration
- **SEO Optimized**: Meta tags, sitemap, and semantic HTML
- **Secure**: CSRF protection, password hashing, rate limiting

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5.3
- Font Awesome 6
- Google Fonts (Playfair Display, Poppins)
- AOS (Animate On Scroll)
- Lightbox2

### Backend
- Python 3.9+
- Flask 3.0
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-Mail (Email)
- Flask-WTF (Forms & CSRF)
- Flask-Migrate (Database migrations)

### Database
- SQLite (Development)
- PostgreSQL (Production ready)

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip
- virtualenv (recommended)

### Setup

1. **Clone the repository**
```bash
cd restaurant_website
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Initialize database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Create admin user**
```bash
python create_admin.py
```

7. **Run the application**
```bash
flask run
```

Visit: http://localhost:5000

## 🗂️ Project Structure

```
restaurant_website/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── routes/               # Route blueprints
│   │   ├── main.py           # Public routes
│   │   ├── admin.py          # Admin routes
│   │   └── api.py            # REST API
│   ├── forms.py              # WTForms
│   ├── utils.py              # Helper functions
│   ├── static/               # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/            # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── menu.html
│       ├── admin/
│       └── components/
├── migrations/               # Database migrations
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env.example              # Environment template
├── create_admin.py           # Admin setup script
└── run.py                    # Application entry point
```

## 🔐 Admin Access

Default credentials (change immediately):
- **URL**: http://localhost:5000/admin/login
- **Username**: admin
- **Password**: admin123

## 📊 Database Schema

### Users
- id, username, email, password_hash, role, created_at

### Reservations
- id, name, email, phone, date, time, party_size, special_requests, status, created_at

### MenuItems
- id, name, description, price, category, image_url, is_available, created_at

### Categories
- id, name, slug, display_order

### Gallery
- id, title, image_url, description, display_order, created_at

### Reviews
- id, customer_name, rating, comment, is_approved, created_at

### Events
- id, title, description, event_date, image_url, is_active, created_at

## 🚀 Deployment

### Railway / Render

1. **Update requirements.txt with production dependencies**
```bash
pip install gunicorn psycopg2-binary
pip freeze > requirements.txt
```

2. **Create Procfile**
```
web: gunicorn run:app
```

3. **Set environment variables** in platform dashboard

4. **Deploy**

### Traditional VPS (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Setup application
cd /var/www/restaurant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx
sudo nano /etc/nginx/sites-available/restaurant

# Setup SSL with Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

## 🔧 Configuration

Key environment variables in `.env`:

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/dbname
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## 📧 Email Configuration

For Gmail:
1. Enable 2-factor authentication
2. Generate app-specific password
3. Use in MAIL_PASSWORD variable

## 🧪 Testing

```bash
# Run tests
python -m pytest

# Check coverage
pytest --cov=app tests/
```

## 📈 Performance Optimization

- Image optimization with lazy loading
- CSS/JS minification
- Browser caching headers
- Database query optimization
- CDN integration ready

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing with Werkzeug
- SQL injection prevention via ORM
- XSS protection
- Rate limiting on API endpoints
- Secure session management
- HTTPS enforcement (production)

## 📱 Mobile Optimization

- Responsive breakpoints
- Touch-optimized UI
- Mobile menu navigation
- Fast page loads (<2s)
- PWA ready

## ♿ Accessibility

- WCAG 2.1 Level AA compliant
- ARIA labels
- Keyboard navigation
- High contrast support
- Screen reader friendly

## 🐛 Troubleshooting

**Database errors:**
```bash
flask db stamp head
flask db migrate
flask db upgrade
```

**Email not sending:**
- Check SMTP credentials
- Verify firewall/port settings
- Enable "less secure apps" (Gmail)

## 📄 License

MIT License - feel free to use for your restaurant!

## 🤝 Contributing

Contributions welcome! Please open an issue first to discuss changes.

## 📞 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ for restaurants worldwide**
