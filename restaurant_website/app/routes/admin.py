from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from app import db
from app.models import User, Reservation, MenuItem, Category, GalleryImage, Review, Event, ContactMessage
from app.forms import (LoginForm, MenuItemForm, CategoryForm, GalleryForm, EventForm, 
                       UserForm, ReservationUpdateForm)
from app.utils import save_image, delete_image, send_email, create_slug
from datetime import datetime, timedelta
from sqlalchemy import func, and_

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need administrator privileges to access this page.', 'danger')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_reservations = Reservation.query.count()
    pending_reservations = Reservation.query.filter_by(status='pending').count()
    total_menu_items = MenuItem.query.count()
    pending_reviews = Review.query.filter_by(is_approved=False).count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    # Recent reservations
    recent_reservations = Reservation.query.order_by(Reservation.created_at.desc()).limit(5).all()
    
    # Upcoming reservations
    today = datetime.now().date()
    upcoming_reservations = Reservation.query.filter(
        and_(Reservation.date >= today, Reservation.status == 'confirmed')
    ).order_by(Reservation.date, Reservation.time).limit(10).all()
    
    # Recent contact messages
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    # Revenue statistics (example - would need order model)
    stats = {
        'total_reservations': total_reservations,
        'pending_reservations': pending_reservations,
        'total_menu_items': total_menu_items,
        'pending_reviews': pending_reviews,
        'unread_messages': unread_messages
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_reservations=recent_reservations,
                         upcoming_reservations=upcoming_reservations,
                         recent_messages=recent_messages)


# ============ Reservations Management ============

@admin_bp.route('/reservations')
@login_required
def reservations():
    """Manage reservations"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    date_filter = request.args.get('date', '')
    
    query = Reservation.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if date_filter:
        try:
            date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
            query = query.filter_by(date=date_obj)
        except ValueError:
            pass
    
    pagination = query.order_by(Reservation.date.desc(), Reservation.time.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/reservations.html', pagination=pagination)


@admin_bp.route('/reservations/<int:id>/update', methods=['GET', 'POST']) # Added GET
@login_required
def update_reservation(id):
    """Update reservation status"""
    reservation = Reservation.query.get_or_404(id)
    # This assumes you have a form called ReservationUpdateForm
    form = ReservationUpdateForm(obj=reservation) 
    
    if form.validate_on_submit():
        old_status = reservation.status
        reservation.status = form.status.data
        reservation.updated_at = datetime.utcnow()
        db.session.commit()
        
        if old_status != 'confirmed' and form.status.data == 'confirmed':
            from app.utils import send_reservation_confirmation
            send_reservation_confirmation(reservation)
        
        flash(f'Reservation status updated to {form.status.data}', 'success')
        return redirect(url_for('admin.reservations'))
    
    # If it's a GET request, render the new template
    return render_template('admin/update_reservation.html', form=form, reservation=reservation)

@admin_bp.route('/reservations/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_reservation(id):
    """Delete reservation"""
    reservation = Reservation.query.get_or_404(id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Reservation deleted successfully', 'success')
    return redirect(url_for('admin.reservations'))


# ============ Menu Management ============

@admin_bp.route('/menu')
@login_required
def menu():
    """Manage menu items"""
    category_filter = request.args.get('category', type=int)
    
    query = MenuItem.query
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    
    menu_items = query.order_by(MenuItem.category_id, MenuItem.display_order).all()
    categories = Category.query.order_by(Category.display_order).all()
    
    return render_template('admin/menu.html', menu_items=menu_items, categories=categories)


@admin_bp.route('/menu/add', methods=['GET', 'POST'])
@login_required
def add_menu_item():
    """Add new menu item"""
    form = MenuItemForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        menu_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category_id.data,
            is_available=form.is_available.data,
            is_featured=form.is_featured.data,
            allergens=form.allergens.data,
            preparation_time=form.preparation_time.data,
            display_order=form.display_order.data
        )
        
        if form.image.data:
            image_file = save_image(form.image.data, folder='menu')
            menu_item.image_url = image_file
        
        db.session.add(menu_item)
        db.session.commit()
        
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin.menu'))
    
    return render_template('admin/menu_form.html', form=form, title='Add Menu Item')


@admin_bp.route('/menu/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_menu_item(id):
    """Edit menu item"""
    menu_item = MenuItem.query.get_or_404(id)
    form = MenuItemForm(obj=menu_item)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    
    if form.validate_on_submit():
        menu_item.name = form.name.data
        menu_item.description = form.description.data
        menu_item.price = form.price.data
        menu_item.category_id = form.category_id.data
        menu_item.is_available = form.is_available.data
        menu_item.is_featured = form.is_featured.data
        menu_item.allergens = form.allergens.data
        menu_item.preparation_time = form.preparation_time.data
        menu_item.display_order = form.display_order.data
        menu_item.updated_at = datetime.utcnow()
        
        if form.image.data:
            # Delete old image
            if menu_item.image_url:
                delete_image(menu_item.image_url)
            # Save new image
            image_file = save_image(form.image.data, folder='menu')
            menu_item.image_url = image_file
        
        db.session.commit()
        flash('Menu item updated successfully!', 'success')
        return redirect(url_for('admin.menu'))
    
    return render_template('admin/menu_form.html', form=form, title='Edit Menu Item', menu_item=menu_item)


@admin_bp.route('/menu/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_menu_item(id):
    """Delete menu item"""
    menu_item = MenuItem.query.get_or_404(id)
    
    if menu_item.image_url:
        delete_image(menu_item.image_url)
    
    db.session.delete(menu_item)
    db.session.commit()
    
    flash('Menu item deleted successfully', 'success')
    return redirect(url_for('admin.menu'))


# ============ Category Management ============

@admin_bp.route('/categories')
@login_required
def categories():
    """Manage categories"""
    categories = Category.query.order_by(Category.display_order).all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            slug=create_slug(form.name.data),
            description=form.description.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, title='Add Category')


@admin_bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """Edit category"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = create_slug(form.name.data)
        category.description = form.description.data
        category.display_order = form.display_order.data
        category.is_active = form.is_active.data
        
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, title='Edit Category', category=category)


@admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(id):
    """Delete category"""
    category = Category.query.get_or_404(id)
    
    # Check if category has menu items
    if category.menu_items.count() > 0:
        flash('Cannot delete category with menu items. Please reassign or delete the items first.', 'danger')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin.categories'))


# ============ Gallery Management ============

@admin_bp.route('/gallery')
@login_required
def gallery():
    """Manage gallery"""
    images = GalleryImage.query.order_by(GalleryImage.display_order, GalleryImage.created_at.desc()).all()
    return render_template('admin/gallery.html', images=images)


@admin_bp.route('/gallery/add', methods=['GET', 'POST'])
@login_required
def add_gallery_image():
    """Add gallery image"""
    form = GalleryForm()
    
    if form.validate_on_submit():
        image_file = save_image(form.image.data, folder='gallery', size=(1200, 800))
        
        gallery_image = GalleryImage(
            title=form.title.data,
            image_url=image_file,
            description=form.description.data,
            alt_text=form.alt_text.data or form.title.data,
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )
        
        db.session.add(gallery_image)
        db.session.commit()
        
        flash('Image added to gallery!', 'success')
        return redirect(url_for('admin.gallery'))
    
    return render_template('admin/gallery_form.html', form=form, title='Add Image')


@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_gallery_image(id):
    """Delete gallery image"""
    image = GalleryImage.query.get_or_404(id)
    
    delete_image(image.image_url)
    db.session.delete(image)
    db.session.commit()
    
    flash('Image deleted successfully', 'success')
    return redirect(url_for('admin.gallery'))


# ============ Reviews Management ============

@admin_bp.route('/reviews')
@login_required
def reviews():
    """Manage reviews"""
    status_filter = request.args.get('status', 'pending')
    
    if status_filter == 'pending':
        reviews = Review.query.filter_by(is_approved=False).order_by(Review.created_at.desc()).all()
    elif status_filter == 'approved':
        reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).all()
    else:
        reviews = Review.query.order_by(Review.created_at.desc()).all()
    
    return render_template('admin/reviews.html', reviews=reviews, status_filter=status_filter)


@admin_bp.route('/reviews/<int:id>/approve', methods=['POST'])
@login_required
def approve_review(id):
    """Approve review"""
    review = Review.query.get_or_404(id)
    review.is_approved = True
    db.session.commit()
    flash('Review approved!', 'success')
    return redirect(url_for('admin.reviews'))


@admin_bp.route('/reviews/<int:id>/delete', methods=['POST'])
@login_required
def delete_review(id):
    """Delete review"""
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted', 'success')
    return redirect(url_for('admin.reviews'))


# ============ Events Management ============

@admin_bp.route('/events')
@login_required
def events():
    """Manage events"""
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('admin/events.html', events=events)


@admin_bp.route('/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    """Add new event"""
    form = EventForm()
    
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            end_date=form.end_date.data,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data
        )
        
        if form.image.data:
            image_file = save_image(form.image.data, folder='events')
            event.image_url = image_file
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/event_form.html', form=form, title='Add Event')


@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    """Edit event"""
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    
    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.end_date = form.end_date.data
        event.is_active = form.is_active.data
        event.is_featured = form.is_featured.data
        event.updated_at = datetime.utcnow()
        
        if form.image.data:
            if event.image_url:
                delete_image(event.image_url)
            image_file = save_image(form.image.data, folder='events')
            event.image_url = image_file
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/event_form.html', form=form, title='Edit Event', event=event)


@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_event(id):
    """Delete event"""
    event = Event.query.get_or_404(id)
    
    if event.image_url:
        delete_image(event.image_url)
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin.events'))


# ============ Contact Messages ============

@admin_bp.route('/messages')
@login_required
def messages():
    """View contact messages"""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)


# Import the CSRF protection instance from your app
from app import csrf 

@admin_bp.route('/messages/<int:id>/mark-read', methods=['POST'])
@login_required
@csrf.exempt  # <--- Add this decorator here
def mark_message_read(id):
    """Mark message as read"""
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    return redirect(url_for('admin.messages'))


@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
def delete_message(id):
    """Delete contact message"""
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted', 'success')
    return redirect(url_for('admin.messages'))
