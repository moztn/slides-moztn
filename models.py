from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin

class AdministratorModel(Base,UserMixin):
    __tablename__ = 'administrators'
    id = Column(Integer, primary_key=True)
    email = Column(String(90), unique=True)

    def __init__(self, email=None):
        self.email = email

    def __repr__(self):
        return '<Administrator %r>' %(self.email)

class SlideModel(Base):
    __tablename__ = 'slides'
    id = Column(Integer, primary_key=True)
    title = Column(String(15), nullable=False)
    url = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    category = Column(Integer, ForeignKey('categories.id'), nullable=False)
    # category = relationship('Category', backref=backref('slides', lazy='dynamic'))
    screenshot = Column(String(255))

    def __repr__(self):
        return '<Slide %s>' %(self.title)

    # We will use this fonction to generate the githubio url
    # Note that we assume that is a correct github url
    # And the gh-pages branch exists
    # See function isValidURL in slides.py
    @property
    def github_demo_url(self):
        print(self.url[19:].split('/'))
        subdomain, prefix = self.url[19:].split('/')
        return "http://{0}.github.io/{1}".format(subdomain, prefix)

    @property
    def github_download_url(self):
        url = self.url.lower()
        url = url + '/archive/master.zip'
        return url


class CategoryModel(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    # slides = relationship("Slide", backref="categories")

    # def __init__(self, name=None):
    #     self.name = name

    def __repr__(self):
        return '<Category %s>' %(self.name)

