import os
import secrets
from PIL import Image
from flask import current_app, url_for
from flask_mail import Message
from app import mail
from slugify import slugify


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_image(form_image, folder='images', size=(800, 800)):
    """
    Save uploaded image with random filename
    
    Args:
        form_image: FileStorage object from form
        folder: Subfolder in uploads directory
        size: Tuple of (width, height) for resizing
    
    Returns:
        Filename of saved image
    """
    # Generate random filename
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_image.filename)
    filename = random_hex + file_ext
    
    # Create folder path
    folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    file_path = os.path.join(folder_path, filename)
    
    # Resize and save image
    try:
        image = Image.open(form_image)
        
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # Resize maintaining aspect ratio
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save with optimization
        image.save(file_path, quality=85, optimize=True)
        
    except Exception as e:
        current_app.logger.error(f"Error saving image: {str(e)}")
        # Save original if processing fails
        form_image.save(file_path)
    
    return f"{folder}/{filename}"


def delete_image(image_path):
    """Delete image file"""
    if image_path:
        try:
            full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
            if os.path.exists(full_path):
                os.remove(full_path)
        except Exception as e:
            current_app.logger.error(f"Error deleting image: {str(e)}")


def send_email(subject, recipients, text_body=None, html_body=None):
    """
    Send email
    
    Args:
        subject: Email subject
        recipients: List of recipient emails
        text_body: Plain text body
        html_body: HTML body
    """
    try:
        msg = Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        
        if text_body:
            msg.body = text_body
        if html_body:
            msg.html = html_body
        
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False


def send_reservation_confirmation(reservation):
    """Send reservation confirmation email"""
    subject = f"Reservation Confirmation - {current_app.config['RESTAURANT_NAME']}"
    
    text_body = f"""
    Dear {reservation.name},
    
    Thank you for your reservation at {current_app.config['RESTAURANT_NAME']}!
    
    Reservation Details:
    - Date: {reservation.date.strftime('%B %d, %Y')}
    - Time: {reservation.time.strftime('%I:%M %p')}
    - Party Size: {reservation.party_size} guests
    - Status: {reservation.status.title()}
    
    {f"Special Requests: {reservation.special_requests}" if reservation.special_requests else ""}
    
    We look forward to serving you!
    
    If you need to modify or cancel your reservation, please contact us at:
    Phone: {current_app.config['RESTAURANT_PHONE']}
    Email: {current_app.config['RESTAURANT_EMAIL']}
    
    Best regards,
    {current_app.config['RESTAURANT_NAME']} Team
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5f2d;">Reservation Confirmation</h2>
                <p>Dear {reservation.name},</p>
                <p>Thank you for your reservation at <strong>{current_app.config['RESTAURANT_NAME']}</strong>!</p>
                
                <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c5f2d;">Reservation Details</h3>
                    <ul style="list-style: none; padding: 0;">
                        <li><strong>Date:</strong> {reservation.date.strftime('%B %d, %Y')}</li>
                        <li><strong>Time:</strong> {reservation.time.strftime('%I:%M %p')}</li>
                        <li><strong>Party Size:</strong> {reservation.party_size} guests</li>
                        <li><strong>Status:</strong> <span style="color: #2c5f2d;">{reservation.status.title()}</span></li>
                    </ul>
                    {f"<p><strong>Special Requests:</strong> {reservation.special_requests}</p>" if reservation.special_requests else ""}
                </div>
                
                <p>We look forward to serving you!</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p style="font-size: 12px; color: #666;">
                        If you need to modify or cancel your reservation, please contact us:<br>
                        Phone: {current_app.config['RESTAURANT_PHONE']}<br>
                        Email: {current_app.config['RESTAURANT_EMAIL']}
                    </p>
                </div>
                
                <p style="margin-top: 20px;">
                    Best regards,<br>
                    <strong>{current_app.config['RESTAURANT_NAME']} Team</strong>
                </p>
            </div>
        </body>
    </html>
    """
    
    return send_email(subject, reservation.email, text_body, html_body)


def send_contact_notification(message):
    """Send notification about new contact message"""
    subject = f"New Contact Message - {message.subject or 'No Subject'}"
    
    text_body = f"""
    New contact message received:
    
    From: {message.name}
    Email: {message.email}
    Phone: {message.phone or 'Not provided'}
    Subject: {message.subject or 'No subject'}
    
    Message:
    {message.message}
    
    Received at: {message.created_at.strftime('%B %d, %Y at %I:%M %p')}
    """
    
    return send_email(
        subject,
        current_app.config['RESTAURANT_EMAIL'],
        text_body
    )


def create_slug(text):
    """Create URL-friendly slug from text"""
    return slugify(text)


def paginate_query(query, page=1, per_page=12):
    """
    Paginate a SQLAlchemy query
    
    Args:
        query: SQLAlchemy query object
        page: Current page number
        per_page: Items per page
    
    Returns:
        Pagination object
    """
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )


def format_phone(phone):
    """Format phone number"""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Format based on length
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone


def get_image_url(image_path):
    """Get full URL for uploaded image"""
    if not image_path:
        return url_for('static', filename='images/placeholder.jpg')
    return url_for('static', filename=f'uploads/{image_path}')
