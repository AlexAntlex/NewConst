import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    deadline = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    participants = sqlalchemy.Column(sqlalchemy.String(255), nullable=False) # Список участников через запятую
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    user_id_worker = sqlalchemy.Column(sqlalchemy.Integer,
                                       sqlalchemy.ForeignKey("user.id"), nullable=True)
