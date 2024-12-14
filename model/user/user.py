from datetime import datetime
import traceback

from sqlalchemy import Column, Integer, DateTime, Boolean, String
from sqlalchemy.orm import relationship

from database.db_conn import Base, engine
from database.db_session import session
from utils.utility import generate_auto_id, datetime_to_string


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_ag_id = Column(String(150), unique=True, nullable=False)
    username = Column(String(150), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

    is_verified = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    email_verify_tokens = relationship('UserEmailVerifyToken', backref='user',
                                       lazy=True)
    forget_password_tokens = relationship('UserForgetPasswordToken',
                                          backref='user', lazy=True)
    user_details = relationship('UserDetails', backref='user', uselist=False)
    saved_articles = relationship('SavedArticle', backref='user',
                                  lazy=True)

    def __init__(self, user_ag_id=None, username=None, password=None):
        self.user_ag_id = user_ag_id
        self.username = username
        self.password = password

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_ag_id': self.user_ag_id,
            'username': self.username,
            'password': self.password,
            'status': self.status,
            'is_deleted': self.is_deleted,
            'created_at': datetime_to_string(self.created_at),
            'updated_at': datetime_to_string(self.updated_at)
        }


def add_user(username=None, password=None):
    try:
        if not username or not password:
            return False
        user_ag_id = generate_auto_id(prefix="user", length=32)
        user = User(user_ag_id=user_ag_id, username=username,
                    password=password)
        session.add(user)
        session.commit()
        return True
    except:
        print(traceback.format_exc())
        session.rollback()
        return False
    finally:
        session.close()


Base.metadata.create_all(engine)
