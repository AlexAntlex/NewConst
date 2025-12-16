import sqlalchemy


class Message(sqlalchemy.Model):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,primary_key=True)
    sender = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    receiver = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    message = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    file_path = sqlalchemy.Column(sqlalchemy.String(50), nullable=True)