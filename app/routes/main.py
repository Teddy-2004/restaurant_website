from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app import db, limiter
from app.models import MenuItem, Category, GalleryImage, Review, Event, Reservation, ContactMessage
from app.forms import ReservationForm, ContactForm, ReviewForm
from app.utils import send_reservation_confirmation, send_contact_notification
from datetime import datetime
from sqlalchemy import and_

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage"""
    # Get featured menu items
    featured_items = MenuItem.query.filter_by(is_featured=True, is_available=True)\
        .order_by(MenuItem.display_order).limit(6).all()
    
    # Get approved reviews
    reviews = Review.query.filter_by(is_approved=True)\
        .order_by(Review.created_at.desc()).limit(6).all()
    
    # Get upcoming events
    upcoming_events = Event.query.filter(
        and_(Event.is_active == True, Event.event_date >= datetime.utcnow())
    ).order_by(Event.event_date).limit(3).all()
    
    # Get gallery images
    gallery_images = GalleryImage.query.filter_by(is_active=True)\
        .order_by(GalleryImage.display_order).limit(8).all()
    
    return render_template('index.html',
                         featured_items=featured_items,
                         reviews=reviews,
                         upcoming_events=upcoming_events,
                         gallery_images=gallery_images)


@main_bp.route('/menu')
def menu():
    """Menu page"""
    # Get all active categories with their items
    categories = Category.query.filter_by(is_active=True)\
        .order_by(Category.display_order).all()
    
    # Get search and filter parameters
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    
    # Build query
    query = MenuItem.query.filter_by(is_available=True)
    
    if search_query:
        query = query.filter(MenuItem.name.ilike(f'%{search_query}%'))
    
    if category_filter:
        query = query.filter_by(category_id=int(category_filter))
    
    menu_items = query.order_by(MenuItem.category_id, MenuItem.display_order).all()
    
    return render_template('menu.html',
                         categories=categories,
                         menu_items=menu_items,
                         search_query=search_query,
                         category_filter=category_filter)


@main_bp.route('/reservations', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def reservations():
    """Reservations page"""
    form = ReservationForm()
    
    if form.validate_on_submit():
        reservation = Reservation(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            date=form.date.data,
            time=form.time.data,
            party_size=form.party_size.data,
            special_requests=form.special_requests.data,
            status='pending'
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        # Send confirmation email
        send_reservation_confirmation(reservation)
        
        flash('Your reservation has been submitted! We will send you a confirmation email shortly.', 'success')
        return redirect(url_for('main.reservations'))
    
    return render_template('reservations.html', form=form)


@main_bp.route('/gallery')
def gallery():
    """Gallery page"""
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    pagination = GalleryImage.query.filter_by(is_active=True)\
        .order_by(GalleryImage.display_order, GalleryImage.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('gallery.html', pagination=pagination)


@main_bp.route('/events')
def events():
    """Events page"""
    # Get upcoming events
    upcoming = Event.query.filter(
        and_(Event.is_active == True, Event.event_date >= datetime.utcnow())
    ).order_by(Event.event_date).all()
    
    # Get past events
    past = Event.query.filter(
        and_(Event.is_active == True, Event.event_date < datetime.utcnow())
    ).order_by(Event.event_date.desc()).limit(6).all()
    
    return render_template('events.html', upcoming_events=upcoming, past_events=past)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def contact():
    """Contact page"""
    form = ContactForm()
    
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Send notification to restaurant
        send_contact_notification(message)
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)


@main_bp.route('/reviews', methods=['GET', 'POST'])
@limiter.limit("3 per day")
def reviews():
    """Reviews page"""
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            customer_name=form.customer_name.data,
            rating=form.rating.data,
            comment=form.comment.data,
            is_approved=False  # Requires admin approval
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Thank you for your review! It will be published after moderation.', 'success')
        return redirect(url_for('main.reviews'))
    
    # Get approved reviews
    page = request.args.get('page', 1, type=int)
    pagination = Review.query.filter_by(is_approved=True)\
        .order_by(Review.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    # Calculate average rating
    approved_reviews = Review.query.filter_by(is_approved=True).all()
    avg_rating = sum(r.rating for r in approved_reviews) / len(approved_reviews) if approved_reviews else 0
    
    return render_template('reviews.html',
                         form=form,
                         pagination=pagination,
                         avg_rating=avg_rating,
                         total_reviews=len(approved_reviews))


@main_bp.route('/check-availability')
@limiter.limit("30 per minute")
def check_availability():
    """Check table availability (AJAX endpoint)"""
    date_str = request.args.get('date')
    time_str = request.args.get('time')
    party_size = request.args.get('party_size', type=int)
    
    if not all([date_str, time_str, party_size]):
        return jsonify({'available': False, 'message': 'Missing parameters'})
    
    try:
        # Parse date and time
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        # Check existing reservations
        existing = Reservation.query.filter(
            and_(
                Reservation.date == date_obj,
                Reservation.time == time_obj,
                Reservation.status.in_(['pending', 'confirmed'])
            )
        ).count()
        
        # Simple availability logic (max 5 reservations per time slot)
        available = existing < 5
        
        return jsonify({
            'available': available,
            'message': 'Time slot available!' if available else 'This time slot is fully booked. Please choose another time.'
        })
        
    except Exception as e:
        return jsonify({'available': False, 'message': 'Error checking availability'})
