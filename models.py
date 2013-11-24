from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Administrator(Base):
  __tablename__ = 'administrators'
  id = Column(Integer, primary_key=True)
  email = Column(String(90), unique=True)

  def __init__(self, email=None):
    self.email = email

  def __repr__(self):
    return '<Administrator %r>' %(self.email)


class Slide(Base):
  __tablename__ = 'slides'
  id = Column(Integer, primary_key=True)
  title = Column(String(15), nullable=False)
  url = Column(String(255), unique=True, nullable=False)
  description = Column(String(255), nullable=False)
  category = Column(Integer, ForeignKey('categories.id'), nullable=False)
  screenshot = Column(String(255))

  def __init__(self, title, url, description, category, screenshot = None):
    self.title = title
    self.url = url
    self.description = description
    self.category = category
    self.screenshot = screenshot

  def __repr__(self):
    return '<Slide %s>' %(self.title)


class Category(Base):
  __tablename__ = 'categories'
  id = Column(Integer, primary_key=True)
  name = Column(String(255), nullable=False, unique=True)

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return '<Category %s>' %(self.name)

