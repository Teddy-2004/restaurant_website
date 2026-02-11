# 📁 Project Structure

Complete file structure of the restaurant website application.

```
restaurant_website/
│
├── 📄 README.md                    # Main documentation
├── 📄 QUICKSTART.md                # Quick setup guide
├── 📄 DEPLOYMENT.md                # Deployment instructions
├── 📄 API.md                       # API documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 config.py                    # Application configuration
├── 📄 run.py                       # Application entry point
├── 📄 create_admin.py              # Admin setup script
├── 📄 Procfile                     # Deployment configuration
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 app/                         # Main application package
│   ├── 📄 __init__.py             # App factory & initialization
│   ├── 📄 models.py               # Database models
│   ├── 📄 forms.py                # WTForms
│   ├── 📄 utils.py                # Utility functions
│   │
│   ├── 📁 routes/                 # Route blueprints
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py             # Public routes
│   │   ├── 📄 admin.py            # Admin routes
│   │   └── 📄 api.py              # REST API routes
│   │
│   ├── 📁 static/                 # Static files
│   │   ├── 📁 css/
│   │   │   └── 📄 style.css       # Custom stylesheet
│   │   ├── 📁 js/
│   │   │   └── 📄 main.js         # Custom JavaScript
│   │   ├── 📁 images/             # Static images
│   │   └── 📁 uploads/            # User uploads
│   │       ├── 📁 menu/           # Menu item images
│   │       ├── 📁 gallery/        # Gallery images
│   │       └── 📁 events/         # Event images
│   │
│   └── 📁 templates/              # Jinja2 templates
│       ├── 📄 base.html           # Base template
│       ├── 📄 index.html          # Homepage
│       ├── 📄 menu.html           # Menu page
│       ├── 📄 reservations.html   # Reservations page
│       ├── 📄 gallery.html        # Gallery page
│       ├── 📄 events.html         # Events page
│       ├── 📄 about.html          # About page
│       ├── 📄 contact.html        # Contact page
│       ├── 📄 reviews.html        # Reviews page
│       │
│       ├── 📁 admin/              # Admin templates
│       │   ├── 📄 login.html      # Admin login
│       │   ├── 📄 dashboard.html  # Dashboard
│       │   ├── 📄 menu.html       # Menu management
│       │   ├── 📄 menu_form.html  # Menu item form
│       │   ├── 📄 categories.html # Categories management
│       │   ├── 📄 reservations.html # Reservations management
│       │   ├── 📄 gallery.html    # Gallery management
│       │   ├── 📄 reviews.html    # Reviews management
│       │   ├── 📄 events.html     # Events management
│       │   └── 📄 messages.html   # Contact messages
│       │
│       └── 📁 errors/             # Error pages
│           ├── 📄 404.html        # Not found
│           ├── 📄 403.html        # Forbidden
│           └── 📄 500.html        # Server error
│
└── 📁 migrations/                 # Database migrations
    └── 📁 versions/               # Migration versions
```

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation with features, installation, and usage |
| `QUICKSTART.md` | 5-minute setup guide for quick deployment |
| `DEPLOYMENT.md` | Comprehensive deployment guide for various platforms |
| `API.md` | REST API documentation with endpoints and examples |
| `requirements.txt` | Python package dependencies |
| `config.py` | Application configuration classes (Dev, Prod, Test) |
| `run.py` | Application entry point and shell context |
| `create_admin.py` | Script to create admin user and sample data |
| `Procfile` | Deployment configuration for Heroku/Railway |
| `.env.example` | Template for environment variables |
| `.gitignore` | Git ignore patterns |

### Application Package (`app/`)

#### Core Files

| File | Purpose |
|------|---------|
| `__init__.py` | App factory, extension initialization, blueprints |
| `models.py` | SQLAlchemy database models (User, Reservation, MenuItem, etc.) |
| `forms.py` | WTForms for all forms with validation |
| `utils.py` | Helper functions (image upload, email, etc.) |

#### Routes (`app/routes/`)

| File | Purpose |
|------|---------|
| `main.py` | Public routes (homepage, menu, reservations, contact) |
| `admin.py` | Admin panel routes (dashboard, content management) |
| `api.py` | RESTful API endpoints for external access |

#### Static Files (`app/static/`)

| Directory | Contents |
|-----------|----------|
| `css/` | Custom stylesheets with Bootstrap 5 customization |
| `js/` | JavaScript for interactivity and AJAX |
| `images/` | Logo, favicon, and static images |
| `uploads/` | User-uploaded images (menu, gallery, events) |

#### Templates (`app/templates/`)

##### Public Templates

| Template | Purpose |
|----------|---------|
| `base.html` | Master template with navigation and footer |
| `index.html` | Homepage with hero, features, and highlights |
| `menu.html` | Menu display with search and filtering |
| `reservations.html` | Reservation booking form |
| `gallery.html` | Image gallery with lightbox |
| `events.html` | Events listing |
| `about.html` | About page with story and team |
| `contact.html` | Contact form and information |
| `reviews.html` | Customer reviews and ratings |

##### Admin Templates

| Template | Purpose |
|----------|---------|
| `login.html` | Admin authentication |
| `dashboard.html` | Admin overview with stats |
| `menu.html` | Menu items management |
| `categories.html` | Category management |
| `reservations.html` | Reservation management |
| `gallery.html` | Gallery management |
| `reviews.html` | Review moderation |
| `events.html` | Events management |
| `messages.html` | Contact messages inbox |

## Database Models

### User
- Admin and staff authentication
- Role-based access control
- Password hashing

### Reservation
- Table booking system
- Status tracking (pending/confirmed/cancelled)
- Email notifications

### MenuItem
- Menu item details
- Category association
- Availability and featured status
- Allergen information

### Category
- Menu organization
- Slug for URLs
- Display ordering

### GalleryImage
- Image gallery
- Metadata and alt text
- Display ordering

### Review
- Customer testimonials
- Rating (1-5 stars)
- Approval system

### Event
- Event management
- Date/time handling
- Featured events

### ContactMessage
- Contact form submissions
- Read/unread tracking

## Key Features by File

### Authentication & Authorization
- `app/models.py`: User model with password hashing
- `app/routes/admin.py`: Login/logout, admin decorators
- `app/templates/admin/login.html`: Login interface

### Reservation System
- `app/forms.py`: ReservationForm with validation
- `app/routes/main.py`: Reservation submission
- `app/utils.py`: Email confirmation
- `app/templates/reservations.html`: Booking interface

### Content Management
- `app/routes/admin.py`: CRUD operations
- `app/forms.py`: Management forms
- `app/templates/admin/*`: Admin interfaces

### API
- `app/routes/api.py`: RESTful endpoints
- Rate limiting
- JSON responses

### Email System
- `app/utils.py`: Email functions
- Flask-Mail integration
- Template support

### Image Management
- `app/utils.py`: Image upload and processing
- PIL/Pillow for resizing
- Organized upload folders

## Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLite (dev), PostgreSQL (prod)
- **ORM**: SQLAlchemy
- **Migrations**: Flask-Migrate
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Email**: Flask-Mail
- **Rate Limiting**: Flask-Limiter

### Frontend
- **CSS Framework**: Bootstrap 5.3
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Playfair Display, Poppins)
- **Animations**: AOS (Animate On Scroll)
- **Gallery**: Lightbox2
- **JavaScript**: Vanilla JS + jQuery

### Deployment
- **Server**: Gunicorn
- **Platforms**: Railway, Render, Heroku, VPS
- **Database**: PostgreSQL

## Directory Conventions

### File Naming
- Python files: `snake_case.py`
- Templates: `kebab-case.html`
- CSS/JS: `kebab-case.css`, `kebab-case.js`
- Images: `descriptive-name.ext`

### Code Organization
- One blueprint per feature area
- Models in single file for simplicity
- Forms grouped by functionality
- Utilities separated by purpose

### Static Files
- CSS: Custom styles in `style.css`
- JS: Custom scripts in `main.js`
- Images: Organized by type/purpose
- Uploads: User content separate from static

## Environment Variables

Required variables in `.env`:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///restaurant.db
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password
RESTAURANT_NAME=Your Restaurant
RESTAURANT_EMAIL=info@restaurant.com
RESTAURANT_PHONE=+1 (555) 123-4567
```

## Database Schema

### Relationships
- Category → MenuItem (one-to-many)
- All models have timestamps
- Cascade deletes where appropriate
- Indexes on frequently queried fields

## Security Features

- CSRF protection on all forms
- Password hashing (Werkzeug)
- SQL injection prevention (ORM)
- XSS protection (Jinja2 auto-escaping)
- Rate limiting on API/forms
- Secure session management
- File upload validation

## Performance Optimizations

- Image compression and resizing
- Lazy loading for images
- Minified CSS/JS (production)
- Database query optimization
- Proper indexing
- Browser caching headers

---

This structure supports:
✅ Easy development and maintenance
✅ Clear separation of concerns
✅ Scalable architecture
✅ Production-ready deployment
✅ SEO optimization
✅ Security best practices
✅ Mobile responsiveness
