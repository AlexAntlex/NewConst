from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField


class DraftForm(FlaskForm):
    file_url = FileField(validators=[FileRequired()])
    submit = SubmitField('Загрузить')