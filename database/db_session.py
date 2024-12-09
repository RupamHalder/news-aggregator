from database.db_conn import engine
from sqlalchemy.orm import sessionmaker, scoped_session

session = scoped_session(sessionmaker(bind=engine))
print("=======================MYSQL SESSION==================================")
