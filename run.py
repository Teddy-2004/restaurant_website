from app import create_app, db
from app.models import User, Reservation, MenuItem, Category, GalleryImage, Review, Event, ContactMessage

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in flask shell"""
    return {
        'db': db,
        'User': User,
        'Reservation': Reservation,
        'MenuItem': MenuItem,
        'Category': Category,
        'GalleryImage': GalleryImage,
        'Review': Review,
        'Event': Event,
        'ContactMessage': ContactMessage
    }


if __name__ == '__main__':
    app.run(debug=True)
