from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, FloatField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask_login import current_user
from Project.models import User

class LoginForm(FlaskForm):
    email=StringField('EMAIL',validators=[DataRequired(),Email()])
    password=PasswordField('PASSWORD', validators=[DataRequired()])
    submit1=SubmitField('LOGIN')

class RegistrationForm(FlaskForm):
    fname=StringField('FIRST NAME', validators=[DataRequired()])
    lname=StringField('LAST NAME', validators=[DataRequired()])
    email=StringField('EMAIL',validators=[DataRequired(),Email()])
    password=PasswordField('PASSWORD', validators=[DataRequired()])
    confirm_password=PasswordField('CONFIRM PASSWORD', validators=[DataRequired()])
    phone=StringField('WHATSAPP NUMBER', validators=[DataRequired()])
    address=StringField('ADDRESS', validators=[DataRequired()])

    submit2=SubmitField('SIGN UP')

    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already")
class UploadForm(FlaskForm):
    item_name=StringField('ITEM NAME', validators=[DataRequired()])
    img1 = FileField('image1', validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    img2 = FileField('image2', validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    img3 = FileField('image3', validators=[FileRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    price = StringField('PRICE', validators=[DataRequired()])
    category = SelectField('CATEGORIES', choices=[('Clothing','Clothing'),('Furniture','Furniture'), ('Accessories','Accessories'), ('Stationery','Stationery'),('Electronics','Electronics'), ('Home Appliances','Home Appliances')],validators=[DataRequired()])
    submit3 = SubmitField('UPLOAD')


