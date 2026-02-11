#!/usr/bin/env python3
"""
Script to create an admin user and sample data for the restaurant website
"""

from app import create_app, db
from app.models import User, Category, MenuItem, GalleryImage, Review, Event
from datetime import datetime, timedelta
import os

def create_admin_user():
    """Create admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print("⚠️  Admin user already exists!")
            response = input("Do you want to reset the password? (y/n): ")
            if response.lower() == 'y':
                admin.set_password('admin123')
                db.session.commit()
                print("✅ Admin password reset to 'admin123'")
        else:
            # Create admin user
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                role='admin',
                is_active=True
            )
            admin.set_password(app.config['ADMIN_PASSWORD'])
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Username: {app.config['ADMIN_USERNAME']}")
            print(f"   Password: {app.config['ADMIN_PASSWORD']}")
            print(f"   Email: {app.config['ADMIN_EMAIL']}")


def create_sample_data():
    """Create sample data for testing"""
    app = create_app()
    
    with app.app_context():
        print("\n📊 Creating sample data...")
        
        # Create categories
        categories_data = [
            {'name': 'Appetizers', 'description': 'Start your meal with our delicious starters', 'display_order': 1},
            {'name': 'Main Courses', 'description': 'Hearty and flavorful main dishes', 'display_order': 2},
            {'name': 'Salads', 'description': 'Fresh and healthy salad options', 'display_order': 3},
            {'name': 'Desserts', 'description': 'Sweet endings to your meal', 'display_order': 4},
            {'name': 'Beverages', 'description': 'Refreshing drinks and cocktails', 'display_order': 5},
        ]
        
        for cat_data in categories_data:
            if not Category.query.filter_by(name=cat_data['name']).first():
                from app.utils import create_slug
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
        salads = Category.query.filter_by(name='Salads').first()
        desserts = Category.query.filter_by(name='Desserts').first()
        beverages = Category.query.filter_by(name='Beverages').first()
        
        menu_items = [
            # Appetizers
            {'name': 'Mediterranean Mezze Platter', 'description': 'Hummus, baba ganoush, falafel, olives, and warm pita', 
             'price': 14.99, 'category_id': appetizers.id, 'is_featured': True},
            {'name': 'Grilled Halloumi', 'description': 'Cyprus cheese grilled to perfection with honey drizzle', 
             'price': 12.99, 'category_id': appetizers.id},
            {'name': 'Spanakopita', 'description': 'Flaky phyllo pastry filled with spinach and feta cheese', 
             'price': 10.99, 'category_id': appetizers.id},
            
            # Main Courses
            {'name': 'Grilled Lamb Chops', 'description': 'Herb-marinated lamb chops with roasted vegetables', 
             'price': 32.99, 'category_id': mains.id, 'is_featured': True},
            {'name': 'Seafood Paella', 'description': 'Traditional Spanish rice dish with shrimp, mussels, and squid', 
             'price': 28.99, 'category_id': mains.id, 'is_featured': True},
            {'name': 'Chicken Souvlaki', 'description': 'Marinated chicken skewers with tzatziki and rice', 
             'price': 19.99, 'category_id': mains.id},
            {'name': 'Vegetarian Moussaka', 'description': 'Layered eggplant, zucchini, and béchamel sauce', 
             'price': 18.99, 'category_id': mains.id},
            
            # Salads
            {'name': 'Greek Salad', 'description': 'Tomatoes, cucumber, olives, feta cheese, and olive oil', 
             'price': 12.99, 'category_id': salads.id},
            {'name': 'Caesar Salad', 'description': 'Romaine lettuce, parmesan, croutons, and Caesar dressing', 
             'price': 11.99, 'category_id': salads.id},
            
            # Desserts
            {'name': 'Baklava', 'description': 'Sweet phyllo pastry with honey and pistachios', 
             'price': 7.99, 'category_id': desserts.id},
            {'name': 'Tiramisu', 'description': 'Classic Italian coffee-flavored dessert', 
             'price': 8.99, 'category_id': desserts.id},
            
            # Beverages
            {'name': 'Fresh Lemonade', 'description': 'House-made lemonade with mint', 
             'price': 4.99, 'category_id': beverages.id},
            {'name': 'Turkish Coffee', 'description': 'Traditional strong coffee', 
             'price': 3.99, 'category_id': beverages.id},
        ]
        
        for item_data in menu_items:
            if not MenuItem.query.filter_by(name=item_data['name']).first():
                menu_item = MenuItem(**item_data, is_available=True)
                db.session.add(menu_item)
        
        db.session.commit()
        print("✅ Menu items created")
        
        # Create sample reviews
        reviews_data = [
            {'customer_name': 'Sarah Johnson', 'rating': 5, 
             'comment': 'Absolutely amazing! The lamb chops were cooked to perfection and the service was outstanding.', 
             'is_approved': True},
            {'customer_name': 'Michael Chen', 'rating': 5, 
             'comment': 'Best Mediterranean food in town! The mezze platter is a must-try.', 
             'is_approved': True},
            {'customer_name': 'Emily Rodriguez', 'rating': 4, 
             'comment': 'Great atmosphere and delicious food. Will definitely come back!', 
             'is_approved': True},
            {'customer_name': 'David Thompson', 'rating': 5, 
             'comment': 'The seafood paella was incredible! Fresh ingredients and authentic flavors.', 
             'is_approved': True},
        ]
        
        for review_data in reviews_data:
            if not Review.query.filter_by(customer_name=review_data['customer_name']).first():
                review = Review(**review_data)
                db.session.add(review)
        
        db.session.commit()
        print("✅ Reviews created")
        
        # Create sample events
        events_data = [
            {
                'title': 'Wine Tasting Night',
                'description': 'Join us for an evening of fine Mediterranean wines paired with our signature dishes. Expert sommelier will guide you through the tasting.',
                'event_date': datetime.now() + timedelta(days=14),
                'is_active': True,
                'is_featured': True
            },
            {
                'title': 'Live Greek Music Night',
                'description': 'Experience authentic Greek music and dancing while enjoying your favorite Mediterranean dishes.',
                'event_date': datetime.now() + timedelta(days=21),
                'is_active': True
            },
        ]
        
        for event_data in events_data:
            if not Event.query.filter_by(title=event_data['title']).first():
                event = Event(**event_data)
                db.session.add(event)
        
        db.session.commit()
        print("✅ Events created")
        
        print("\n✅ Sample data created successfully!")


if __name__ == '__main__':
    print("🍽️  Restaurant Website - Admin Setup")
    print("=" * 50)
    
    # Create database tables
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Database tables created")
    
    # Create admin user
    create_admin_user()
    
    # Ask if user wants sample data
    print("\n" + "=" * 50)
    response = input("Do you want to create sample data? (y/n): ")
    if response.lower() == 'y':
        create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nYou can now run the application:")
    print("  flask run")
    print("\nOr:")
    print("  python run.py")
    print("\nAdmin login at: http://localhost:5000/admin/login")
    print("=" * 50)
