# Под вопросом
""""Внутри задачи должен быть только текст и нумеровка 
Заголовок (тип задачи?), описание требуемой работы, поля для записи этапов работы при ее выполнении"""""
from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class TaskForm(FlaskForm):
    title = StringField('Номер задачи', validators=[DataRequired()])
    info = TextArea('Информация о задаче',)
    steps = TextArea('Ход выполнения') #Подумать про разделение полей как в 1с
