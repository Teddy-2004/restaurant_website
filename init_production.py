#!/usr/bin/env python3
"""
Non-interactive database initialization for production
"""

from app import create_app, db
from app.models import User, Category, MenuItem, Review, Event
from datetime import datetime, timedelta
import os

def init_database():
    """Initialize database with admin user and optional sample data"""
    
    app = create_app()
    
    with app.app_context():
        print("🔄 Creating database tables...")
        db.create_all()
        print("✅ Database tables created")
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("⚠️  Admin user already exists!")
            print("   Resetting password...")
            admin.set_password('admin123')
            db.session.commit()
            print("✅ Admin password reset to 'admin123'")
        else:
            admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
            admin_email = os.environ.get('ADMIN_EMAIL', 'admin@restaurant.com')
            admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            
            admin = User(
                username=admin_username,
                email=admin_email,
                role='admin',
                is_active=True
            )
            admin.set_password(admin_password)
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Username: {admin_username}")
            print(f"   Password: {admin_password}")
            print(f"   Email: {admin_email}")
        
        # Create sample data if needed (only if no categories exist)
        if Category.query.count() == 0:
            print("\n📊 Creating sample data...")
            create_sample_data()
        else:
            print("\n⚠️  Sample data already exists, skipping...")
        
        print("\n✅ Database initialization complete!")
        print(f"\n🌐 Login at: /admin/login")
        print(f"   Username: admin")
        print(f"   Password: admin123")


def create_sample_data():
    """Create sample categories and menu items"""
    from app.utils import create_slug
    
    # Create categories
    categories_data = [
        {'name': 'Appetizers', 'description': 'Start your meal with our delicious starters', 'display_order': 1},
        {'name': 'Main Courses', 'description': 'Hearty and flavorful main dishes', 'display_order': 2},
        {'name': 'Salads', 'description': 'Fresh and healthy salad options', 'display_order': 3},
        {'name': 'Desserts', 'description': 'Sweet endings to your meal', 'display_order': 4},
        {'name': 'Beverages', 'description': 'Refreshing drinks and cocktails', 'display_order': 5},
    ]
    
    for cat_data in categories_data:
        category = Category(
            name=cat_data['name'],
            slug=create_slug(cat_data['name']),
            description=cat_data['description'],
            display_order=cat_data['display_order'],
            is_active=True
        )
        db.session.add(category)
    
    db.session.commit()
    print("✅ Categories created")
    
    # Create sample menu items
    appetizers = Category.query.filter_by(name='Appetizers').first()
    mains = Category.query.filter_by(name='Main Courses').first()
    
    menu_items = [
        {'name': 'Mediterranean Mezze Platter', 'description': 'Hummus, baba ganoush, falafel, olives, and warm pita', 
         'price': 14.99, 'category_id': appetizers.id, 'is_featured': True, 'is_available': True},
        {'name': 'Grilled Lamb Chops', 'description': 'Herb-marinated lamb chops with roasted vegetables', 
         'price': 32.99, 'category_id': mains.id, 'is_featured': True, 'is_available': True},
        {'name': 'Seafood Paella', 'description': 'Traditional Spanish rice dish with shrimp, mussels, and squid', 
         'price': 28.99, 'category_id': mains.id, 'is_featured': True, 'is_available': True},
    ]
    
    for item_data in menu_items:
        menu_item = MenuItem(**item_data)
        db.session.add(menu_item)
    
    db.session.commit()
    print("✅ Menu items created")
    
    # Create sample reviews
    reviews_data = [
        {'customer_name': 'Sarah Johnson', 'rating': 5, 
         'comment': 'Absolutely amazing! The food was incredible and service outstanding.', 
         'is_approved': True},
        {'customer_name': 'Michael Chen', 'rating': 5, 
         'comment': 'Best Mediterranean food in town! Highly recommend the mezze platter.', 
         'is_approved': True},
    ]
    
    for review_data in reviews_data:
        review = Review(**review_data)
        db.session.add(review)
    
    db.session.commit()
    print("✅ Reviews created")


if __name__ == '__main__':
    init_database()