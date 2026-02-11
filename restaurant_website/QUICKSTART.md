# ⚡ Quick Start Guide

Get your restaurant website running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git (optional)

## Step 1: Download & Extract

Extract the project folder to your desired location.

## Step 2: Create Virtual Environment

```bash
# Navigate to project folder
cd restaurant_website

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Setup Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your preferred text editor
# Update at minimum: SECRET_KEY, MAIL settings
```

## Step 5: Initialize Database

```bash
# Initialize database and create admin user
python create_admin.py

# When prompted:
# - Press Enter to create admin user
# - Type 'y' to create sample data (recommended for testing)
```

## Step 6: Run the Application

```bash
# Start the Flask development server
flask run

# Or use:
python run.py
```

## Step 7: Access the Website

Open your browser and visit:

- **Public Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login

### Default Admin Credentials:
- **Username**: admin
- **Password**: admin123

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

## Step 8: Customize

1. **Upload Logo & Images**:
   - Place images in `app/static/images/`
   - Update references in templates

2. **Update Restaurant Info**:
   - Edit `.env` file:
     ```
     RESTAURANT_NAME=Your Restaurant Name
     RESTAURANT_EMAIL=your@email.com
     RESTAURANT_PHONE=+1 (555) 123-4567
     RESTAURANT_ADDRESS=Your Address
     ```

3. **Customize Colors**:
   - Edit `app/static/css/style.css`
   - Modify `:root` variables

4. **Add Content via Admin Panel**:
   - Login to admin
   - Add menu items, categories, events, gallery images

## Common Commands

```bash
# Run development server
flask run

# Run with specific host/port
flask run --host=0.0.0.0 --port=8000

# Database migrations
flask db init
flask db migrate -m "message"
flask db upgrade

# Create new admin user
python create_admin.py

# Access Python shell with models loaded
flask shell
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
flask run --port=8000
```

### Database Errors
```bash
# Delete database and recreate
rm restaurant.db
python create_admin.py
```

### Module Not Found Errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Email Not Working
- Check SMTP settings in `.env`
- For Gmail:
  1. Enable 2-factor authentication
  2. Generate app-specific password
  3. Use app password in `.env`

## Next Steps

1. **Add Content**: Use admin panel to populate your website
2. **Customize Design**: Update colors, fonts, and images
3. **Test Features**: Try all forms and functionality
4. **Deploy**: Follow `DEPLOYMENT.md` for production deployment

## Getting Help

- Check `README.md` for detailed documentation
- Review `DEPLOYMENT.md` for deployment guides
- Open an issue on GitHub for support

## File Structure Overview

```
restaurant_website/
├── app/                    # Application code
│   ├── routes/            # URL routes
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   ├── models.py          # Database models
│   ├── forms.py           # WTForms
│   └── utils.py           # Helper functions
├── config.py              # Configuration
├── run.py                 # Application entry point
├── create_admin.py        # Admin setup script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Features Checklist

After setup, verify these features work:

- [ ] Homepage loads correctly
- [ ] Menu page displays items
- [ ] Reservation form submits
- [ ] Contact form works
- [ ] Admin login successful
- [ ] Can add/edit menu items
- [ ] Can manage reservations
- [ ] Email notifications send
- [ ] Gallery displays images
- [ ] Events page shows events

---

**Congratulations! Your restaurant website is ready! 🎉**

For production deployment, see `DEPLOYMENT.md`.
