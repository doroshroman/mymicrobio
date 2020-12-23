from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, ValidationError, Regexp
from .models import User
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        InputRequired('A password is required')
        ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25,
                                              message='This field length must be between 4 and 25 characters'),
                                              DataRequired('This field is required'),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only '
                                              'letters, numbers, dots or '
                                              'underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6, 
                                                    message='This field length must be more 5 characters'),
                                                    DataRequired('This field is required')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25,
                                              message='This field length must be between 4 and 25 characters'),
                                              DataRequired('This field is required'),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only '
                                              'letters, numbers, dots or '
                                              'underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Picture', validators=[FileAllowed(['jpg', 'png'])])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=200)])
    password = PasswordField('Change Password', validators=[Length(min=6, message='This field length must be more 5 characters')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please choose another username!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is taken. Please choose another email!')


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Empty title! Are you serious?'), Length(max=100,
                                 message='Maximum 100 characters!')])
    
    body = TextAreaField('Content', validators=[DataRequired('Bro, add some content.'), Length(max=140,
                                 message='Maximum 140 characters!')])
    
    submit = SubmitField('Post')


class UpdatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired('Empty title! Are you serious?'), Length(max=100,
                                 message='Maximum 100 characters!')])
    
    body = TextAreaField('Content', validators=[DataRequired('Bro, add some content.'), Length(max=140,
                                 message='Maximum 140 characters!')])
    
    submit = SubmitField('Update')


class AdminUserCreateForm(RegistrationForm):
    admin = BooleanField('Is Admin?', default="checked")
    submit = SubmitField('Create')


class AdminUserUpdateForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=4, max=25,
                                              message='This field length must be between 4 and 25 characters'),
                                              DataRequired('This field is required'),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Username must have only '
                                              'letters, numbers, dots or '
                                              'underscores')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    admin = BooleanField('Is Admin?', default="checked")
    submit = SubmitField('Edit')