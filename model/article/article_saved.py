from datetime import datetime
import traceback

from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey

from database.db_conn import Base, engine
from database.db_session import session
from utils.utility import generate_auto_id, datetime_to_string


class SavedArticle(Base):
    __tablename__ = 'article_saved'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(150), ForeignKey('user.user_ag_id'), nullable=False)
    saved_article_ag_id = Column(String(150), unique=True, nullable=False)
    title = Column(String(300), nullable=False)
    url = Column(String(300), nullable=False)
    category = Column(String(50), nullable=False)
    sentiment = Column(String(50), nullable=True)

    status = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, user_id=None, saved_article_ag_id=None, title=None,
                 url=None, category=None, sentiment=None):
        self.user_id = user_id
        self.saved_article_ag_id = saved_article_ag_id
        self.title = title
        self.url = url
        self.category = category
        self.sentiment = sentiment

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'saved_article_ag_id': self.saved_article_ag_id,
            'title': self.title,
            'url': self.url,
            'category': self.category,
            'sentiment': self.sentiment,
            'status': self.status,
            'is_deleted': self.is_deleted,
            'created_at': datetime_to_string(self.created_at),
            'updated_at': datetime_to_string(self.updated_at)
        }


def add_saved_article(user_id=None, title=None,
                      url=None, category=None, sentiment=None):
    try:
        if not user_id or not title or not url or not category:
            return False
        saved_article_ag_id = generate_auto_id(
            prefix="article_saved", length=32)
        saved_article = SavedArticle(
            user_id=user_id, saved_article_ag_id=saved_article_ag_id,
            title=title, url=url, category=category, sentiment=sentiment)
        session.add(saved_article)
        session.commit()
        return True
    except:
        print(traceback.format_exc())
        session.rollback()
        return False
    finally:
        session.close()


Base.metadata.create_all(engine)
