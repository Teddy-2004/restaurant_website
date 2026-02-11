from flask import Blueprint, jsonify, request
from app import db, limiter
from app.models import MenuItem, Category, Review, Event, Reservation
from datetime import datetime
from sqlalchemy import and_

api_bp = Blueprint('api', __name__)


@api_bp.route('/menu')
@limiter.limit("100 per minute")
def get_menu():
    """Get all menu items (API endpoint)"""
    category_id = request.args.get('category_id', type=int)
    featured_only = request.args.get('featured', type=bool, default=False)
    
    query = MenuItem.query.filter_by(is_available=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if featured_only:
        query = query.filter_by(is_featured=True)
    
    items = query.order_by(MenuItem.category_id, MenuItem.display_order).all()
    
    return jsonify({
        'success': True,
        'count': len(items),
        'items': [item.to_dict() for item in items]
    })


@api_bp.route('/menu/<int:id>')
@limiter.limit("100 per minute")
def get_menu_item(id):
    """Get single menu item"""
    item = MenuItem.query.get_or_404(id)
    
    if not item.is_available:
        return jsonify({'success': False, 'message': 'Item not available'}), 404
    
    return jsonify({
        'success': True,
        'item': item.to_dict()
    })


@api_bp.route('/categories')
@limiter.limit("100 per minute")
def get_categories():
    """Get all categories"""
    categories = Category.query.filter_by(is_active=True)\
        .order_by(Category.display_order).all()
    
    return jsonify({
        'success': True,
        'categories': [{
            'id': c.id,
            'name': c.name,
            'slug': c.slug,
            'description': c.description,
            'item_count': c.menu_items.filter_by(is_available=True).count()
        } for c in categories]
    })


@api_bp.route('/reviews')
@limiter.limit("100 per minute")
def get_reviews():
    """Get approved reviews"""
    limit = request.args.get('limit', 10, type=int)
    limit = min(limit, 50)  # Max 50 reviews
    
    reviews = Review.query.filter_by(is_approved=True)\
        .order_by(Review.created_at.desc())\
        .limit(limit).all()
    
    avg_rating = db.session.query(db.func.avg(Review.rating))\
        .filter_by(is_approved=True).scalar() or 0
    
    return jsonify({
        'success': True,
        'count': len(reviews),
        'average_rating': round(avg_rating, 2),
        'reviews': [review.to_dict() for review in reviews]
    })


@api_bp.route('/events')
@limiter.limit("100 per minute")
def get_events():
    """Get upcoming events"""
    upcoming_only = request.args.get('upcoming', type=bool, default=True)
    
    query = Event.query.filter_by(is_active=True)
    
    if upcoming_only:
        query = query.filter(Event.event_date >= datetime.utcnow())
    
    events = query.order_by(Event.event_date).all()
    
    return jsonify({
        'success': True,
        'count': len(events),
        'events': [event.to_dict() for event in events]
    })


@api_bp.route('/reservations/check', methods=['POST'])
@limiter.limit("30 per minute")
def check_reservation_availability():
    """Check if reservation slot is available"""
    data = request.get_json()
    
    required_fields = ['date', 'time', 'party_size']
    if not all(field in data for field in required_fields):
        return jsonify({
            'success': False,
            'message': 'Missing required fields'
        }), 400
    
    try:
        # Parse date and time
        date_obj = datetime.strptime(data['date'], '%Y-%m-%d').date()
        time_obj = datetime.strptime(data['time'], '%H:%M').time()
        party_size = int(data['party_size'])
        
        # Check if date is in the past
        if date_obj < datetime.now().date():
            return jsonify({
                'success': False,
                'available': False,
                'message': 'Cannot book reservations in the past'
            })
        
        # Check existing reservations
        existing_count = Reservation.query.filter(
            and_(
                Reservation.date == date_obj,
                Reservation.time == time_obj,
                Reservation.status.in_(['pending', 'confirmed'])
            )
        ).count()
        
        # Simple capacity check (max 5 reservations per slot)
        max_reservations_per_slot = 5
        available = existing_count < max_reservations_per_slot
        
        return jsonify({
            'success': True,
            'available': available,
            'message': 'Time slot available' if available else 'This time slot is fully booked',
            'reservations_count': existing_count,
            'max_capacity': max_reservations_per_slot
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'message': 'Invalid date or time format'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error checking availability'
        }), 500


@api_bp.route('/search')
@limiter.limit("60 per minute")
def search():
    """Search menu items"""
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
        }), 400
    
    if len(query) < 2:
        return jsonify({
            'success': False,
            'message': 'Search query must be at least 2 characters'
        }), 400
    
    # Search in menu items
    items = MenuItem.query.filter(
        and_(
            MenuItem.is_available == True,
            db.or_(
                MenuItem.name.ilike(f'%{query}%'),
                MenuItem.description.ilike(f'%{query}%')
            )
        )
    ).order_by(MenuItem.name).limit(20).all()
    
    return jsonify({
        'success': True,
        'query': query,
        'count': len(items),
        'results': [item.to_dict() for item in items]
    })


@api_bp.route('/stats')
@limiter.limit("30 per minute")
def get_stats():
    """Get public statistics"""
    total_reviews = Review.query.filter_by(is_approved=True).count()
    avg_rating = db.session.query(db.func.avg(Review.rating))\
        .filter_by(is_approved=True).scalar() or 0
    total_menu_items = MenuItem.query.filter_by(is_available=True).count()
    upcoming_events = Event.query.filter(
        and_(Event.is_active == True, Event.event_date >= datetime.utcnow())
    ).count()
    
    return jsonify({
        'success': True,
        'stats': {
            'total_reviews': total_reviews,
            'average_rating': round(avg_rating, 2),
            'total_menu_items': total_menu_items,
            'upcoming_events': upcoming_events
        }
    })


# Error handlers for API
@api_bp.errorhandler(404)
def api_not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404


@api_bp.errorhandler(500)
def api_internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


@api_bp.errorhandler(429)
def api_rate_limit_exceeded(error):
    return jsonify({
        'success': False,
        'message': 'Rate limit exceeded. Please try again later.'
    }), 429
