import traceback

from sqlalchemy import Column, Integer, Text, String, ForeignKey

from database.db_conn import Base, engine
from database.db_session import session


class UserForgotPasswordToken(Base):
    __tablename__ = 'user_forgot_password_token'

    id = Column(Integer, primary_key=True)
    user_ag_id = Column(String(150), ForeignKey('user.user_ag_id'), nullable=False)
    token = Column(String(255), nullable=False)
    token_exp_timestamp = Column(Text, nullable=False)
    token_request_count = Column(Integer, default=0)
    next_token_request_timestamp = Column(Text, nullable=True)

    def __init__(self, user_ag_id=None, token=None,
                 token_exp_timestamp=None, token_request_count=0,
                 next_token_request_timestamp=None):
        self.user_ag_id = user_ag_id
        self.token = token
        self.token_exp_timestamp = token_exp_timestamp
        self.token_request_count = token_request_count
        self.next_token_request_timestamp = next_token_request_timestamp

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_ag_id': self.user_ag_id,
            'token': self.token,
            'token_exp_timestamp': self.token_exp_timestamp,
            'token_request_count': self.token_request_count,
            'next_token_request_timestamp': self.next_token_request_timestamp
        }

def add_forget_password_token(user_ag_id, token,
                              token_exp_timestamp, token_request_count,
                              next_token_request_timestamp):
    try:
        fogot_password_token = UserForgotPasswordToken(
            user_ag_id=user_ag_id, token=token,
            token_exp_timestamp=token_exp_timestamp,
            token_request_count=token_request_count,
            next_token_request_timestamp=next_token_request_timestamp)
        session.add(fogot_password_token)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return False
    finally:
        session.close()

Base.metadata.create_all(engine)
