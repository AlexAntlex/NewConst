from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers


class LoginForm(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Войти')

    def validate_phone(form, field):
        if len(field.data) > 16 or len(field.data) < 9:
            raise ValidationError('! Недопустимый номер телефона')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('! Недопустимый номер телефона')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('! Недопустимый номер телефона')