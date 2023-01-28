from sqlalchemy import Column, ForeignKey, Integer, String

from database import Base

class Products(Base):
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    dir_1 = Column(String)
    dir_2 = Column(String)
    discount = Column(Integer)
    rank = Column(Integer)
    price_in = Column(Integer)
    price_out = Column(Integer)
    options = Column(String)
    photo_url = Column(String)
    type = Column(Integer, ForeignKey("types.id"))

class Types(Base):
  __tablename__ = "types"
  __table_args__ = {'extend_existing': True}

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  show = Column(Integer)
  link = Column(String)
  icon = Column(String)
  active = Column(Integer)
  new = Column(Integer)

class Login(Base):
    __tablename__ = "login"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    pwd = Column(String)
