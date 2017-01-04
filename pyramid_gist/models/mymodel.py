from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Integer)
    fname = Column(Text)
    lname = Column(Text)
    ffood = Column(Text)


Index('my_index', MyModel.fname, unique=True, mysql_length=255)
