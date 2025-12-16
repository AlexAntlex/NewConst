import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class TaskComment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'task_step'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    task_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Task.id"), nullable=False)
    author = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    comment = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

