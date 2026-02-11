from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, \
    IntegerField, FloatField, DateField, TimeField, DateTimeField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
from datetime import datetime, date, time


class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')


class ReservationForm(FlaskForm):
    """Reservation booking form"""
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    party_size = IntegerField('Party Size', validators=[DataRequired(), NumberRange(min=1, max=20)])
    special_requests = TextAreaField('Special Requests', validators=[Optional(), Length(max=500)])
    
    def validate_date(self, field):
        if field.data < date.today():
            raise ValidationError('Please select a future date.')
    
    def validate_time(self, field):
        # Check if the date is today and time is in the past
        if self.date.data == date.today():
            now = datetime.now().time()
            if field.data < now:
                raise ValidationError('Please select a future time.')


class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])


class MenuItemForm(FlaskForm):
    """Menu item form"""
    name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    is_available = BooleanField('Available')
    is_featured = BooleanField('Featured Item')
    allergens = StringField('Allergens (comma-separated)', validators=[Optional(), Length(max=255)])
    preparation_time = IntegerField('Preparation Time (minutes)', validators=[Optional(), NumberRange(min=0)])
    display_order = IntegerField('Display Order', validators=[Optional()], default=0)


class CategoryForm(FlaskForm):
    """Category form"""
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    display_order = IntegerField('Display Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active')


class GalleryForm(FlaskForm):
    """Gallery image form"""
    title = StringField('Title', validators=[Optional(), Length(max=100)])
    image = FileField('Image', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    alt_text = StringField('Alt Text', validators=[Optional(), Length(max=255)])
    display_order = IntegerField('Display Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)


class ReviewForm(FlaskForm):
    """Review form"""
    customer_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    rating = SelectField('Rating', 
                        choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')],
                        coerce=int,
                        validators=[DataRequired()])
    comment = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=1000)])


class EventForm(FlaskForm):
    """Event form"""
    title = StringField('Event Title', validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=2000)])
    event_date = DateTimeField('Event Date & Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    end_date = DateTimeField('End Date & Time', validators=[Optional()], format='%Y-%m-%dT%H:%M')
    image = FileField('Event Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    is_active = BooleanField('Active', default=True)
    is_featured = BooleanField('Featured Event')
    
    def validate_event_date(self, field):
        if field.data < datetime.now():
            raise ValidationError('Event date must be in the future.')
    
    def validate_end_date(self, field):
        if field.data and self.event_date.data:
            if field.data < self.event_date.data:
                raise ValidationError('End date must be after start date.')


class UserForm(FlaskForm):
    """User management form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    role = SelectField('Role', 
                      choices=[('admin', 'Administrator'), ('staff', 'Staff')],
                      validators=[DataRequired()])
    is_active = BooleanField('Active', default=True)


class ReservationUpdateForm(FlaskForm):
    """Form for updating reservation status"""
    status = SelectField('Status',
                        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                        validators=[DataRequired()])
