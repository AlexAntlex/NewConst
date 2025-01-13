import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Draft(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'drafts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    way_to_file = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    original_extension = sqlalchemy.Column(sqlalchemy.String)
    upload_date = sqlalchemy.Column(sqlalchemy.Date)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("user.id"), nullable=True)
