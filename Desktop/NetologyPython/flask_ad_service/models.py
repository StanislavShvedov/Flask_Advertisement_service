import sqlalchemy as sq
import atexit
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER', 'user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '1234')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')

PG_DSN = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
engine = create_engine(PG_DSN)

Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=30), nullable=False)
    password = sq.Column(sq.String(length=20), nullable=False)
    email = sq.Column(sq.String(length=50), nullable=False, unique=True)
    reg_time = sq.Column(sq.DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    @property
    def dict(self):
        return {
            'ID-пользователя': self.id,
            'имя': self.name,
            'email': self.email,
            'дата регистрации': self.reg_time.isoformat()
        }

class Advertisement(Base):
    __tablename__ = 'advertisement'

    id = sq.Column(sq.Integer, primary_key=True)
    header = sq.Column(sq.String(length=30), nullable=False)
    description = sq.Column(sq.Text)
    created_at = sq.Column(sq.DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id'), nullable=False)

    user = relationship(User, backref='advertisement')

    @property
    def dict(self):
        return {
            'ID-объявления': self.id,
            'название': self.header,
            'владелец': self.id_user,
            'описание': self.description,
            'создано': self.created_at.isoformat()
        }

def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    atexit.register(engine.dispose)

create_table(engine)
