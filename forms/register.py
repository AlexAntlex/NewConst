import phonenumbers
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField,SelectField, EmailField
from wtforms.validators import DataRequired, ValidationError


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    position = SelectField('Position', choices=[('Младший инженер', 'Младший инженер'), ('Инженер', 'Инженер'),
                                                ('Старший инженер', 'Старший инженер')])

    submit = SubmitField('Войти')

    def validate_phone(form, field):
        if len(field.data) > 16 or len(field.data) < 9:
            raise ValidationError('Недопустимый номер телефона')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Недопустимый номер телефона')
        except:
            input_number = phonenumbers.parse("+1" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Недопустимый номер телефона')
