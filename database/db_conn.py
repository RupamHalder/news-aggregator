from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from conf_enviroment.conf_env import config

engine = create_engine(
    'mysql+pymysql://' + config.DB_USERNAME + ':' + config.DB_PASSWORD + '@' +\
    config.DB_HOST + '/' + config.DB_NAME + '?charset=utf8mb4', echo=False,
    pool_size=20, max_overflow=10, pool_pre_ping=True, pool_recycle=360)

Base = declarative_base()
print("=======================MYSQL CONNECT==================================")
