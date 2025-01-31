import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    text_task = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Date)

    user_id_worker = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("user.id"), nullable=True)
    text_steps = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("task_step.id"), nullable=True)
