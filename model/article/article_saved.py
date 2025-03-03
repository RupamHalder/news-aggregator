from datetime import datetime
import traceback

from sqlalchemy import Column, Integer, DateTime, Boolean, String, ForeignKey, \
    Text, and_

from database.db_conn import Base, engine
from database.db_session import session
from utils.utility import convert_str_to_float, generate_auto_id, \
    datetime_to_string

from model.user.user import User


class SavedArticle(Base):
    __tablename__ = 'article_saved'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(150), ForeignKey('user.user_ag_id'),
                     nullable=False)
    saved_article_ag_id = Column(String(150), unique=True, nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    article_image_url = Column(Text, nullable=True)
    url = Column(String(300), nullable=False)
    sentiment = Column(String(50), nullable=True)
    published_at = Column(String(150), nullable=True)

    status = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, user_id=None, saved_article_ag_id=None, title=None,
                 description=None, article_image_url=None, url=None,
                 sentiment=None, published_at=None):
        self.user_id = user_id
        self.saved_article_ag_id = saved_article_ag_id
        self.title = title
        self.description = description
        self.article_image_url = article_image_url
        self.url = url
        self.sentiment = sentiment
        self.published_at = published_at

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'saved_article_ag_id': self.saved_article_ag_id,
            'title': self.title,
            'description': self.description,
            'article_image_url': self.article_image_url,
            'url': self.url,
            'sentiment': convert_str_to_float(self.sentiment),
            'published_at': self.published_at,
            'status': self.status,
            'is_deleted': self.is_deleted,
            'created_at': datetime_to_string(self.created_at),
            'updated_at': datetime_to_string(self.updated_at)
        }


def add_saved_article(user_id, title, description,
                      article_image_url, url, sentiment, published_at):
    try:
        saved_article_ag_id = generate_auto_id(
            prefix="article_saved", length=32)
        saved_article = SavedArticle(
            user_id=user_id, saved_article_ag_id=saved_article_ag_id,
            title=title, description=description,
            article_image_url=article_image_url,
            url=url, sentiment=sentiment, published_at=published_at)
        session.add(saved_article)
        session.commit()
        return True
    except:
        print(traceback.format_exc())
        session.rollback()
        return False
    finally:
        session.close()


def update_article_table_single_row_data(field_values, field_names,
                                         update_data):
    try:
        filter_condition = [
            getattr(SavedArticle, field_name) == field_value for
            field_value, field_name in zip(field_values, field_names)]
        # Use dynamic filtering based on the provided field name
        article = session.query(SavedArticle).filter(
            and_(*filter_condition),
            SavedArticle.is_deleted == 0,
            SavedArticle.status == 1).first()
        if article is not None:
            for key, value in update_data.items():
                setattr(article, key, value)
            session.commit()
            return True
        else:
            return False
    except:
        session.rollback()
        print("Error in update_is_verified model function:")
        print(traceback.format_exc())
        return False
    finally:
        session.close()


def get_all_article_by_field(field_name, field_value):
    try:
        saved_articles = session.query(SavedArticle).filter(
            getattr(SavedArticle, field_name) == field_value,
            SavedArticle.is_deleted == 0,
            SavedArticle.status == 1).all()

        return [article.serialize for article in saved_articles]
    except:
        print(traceback.format_exc())
        session.rollback()
        return []
    finally:
        session.close()


def is_article_table_field_exist(field_values, field_names):
    try:
        filter_condition = [
            getattr(SavedArticle, field_name) == field_value for
            field_value, field_name in zip(field_values, field_names)]
        # Use dynamic filtering based on the provided field name
        user_count = session.query(SavedArticle).filter(
            and_(*filter_condition),
            SavedArticle.is_deleted == 0,
            SavedArticle.status == 1).count()
        return user_count > 0
    except AttributeError:
        print(
            f"Error: Field '{field_names}' does not exist in the SavedArticle model.")
        return False
    except:
        print(traceback.format_exc())
        session.rollback()
        return False
    finally:
        session.close()


Base.metadata.create_all(engine)
