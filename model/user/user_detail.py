import traceback

from sqlalchemy import Column, Integer, Text, String, ForeignKey

from database.db_conn import Base, engine
from database.db_session import session


class UserDetails(Base):
    __tablename__ = 'user_details'

    id = Column(Integer, primary_key=True)
    user_ag_id = Column(String(150), ForeignKey('user.user_ag_id'), unique=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=True)
    phone_no = Column(String(15), nullable=True)
    profile_pic = Column(Text, nullable=True)

    def __init__(self, user_ag_id=None, first_name=None,
                 last_name=None, phone_no=None, profile_pic=None):
        self.user_ag_id = user_ag_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_no = phone_no
        self.profile_pic = profile_pic

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_ag_id': self.user_ag_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_no': self.phone_no,
            'profile_pic': self.profile_pic
        }


def add_user_details(user_ag_id, first_name, last_name, phone_no, profile_pic):
    try:
        user_detail = UserDetails(
            user_ag_id=user_ag_id, first_name=first_name,
            last_name=last_name, phone_no=phone_no,
            profile_pic=profile_pic)
        session.add(user_detail)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        traceback.print_exc()
        return False
    finally:
        session.close()


Base.metadata.create_all(engine)
