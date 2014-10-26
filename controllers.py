from models import AdministratorModel, SlideModel, CategoryModel
from database import db_session
import logging
from flask import current_app

# logger = current_app.logger


class BaseController(object):
    """
    Base Controller Class.
    """

    model = None

    def create(self, **kwargs):
        """
        Creates new object.
        """
        current_app.logger.info("info")
        current_app.logger.debug("debug")
        print("data = ")
        print(kwargs)
        obj = self.model(**kwargs)
        db_session.add(obj)
        try:
            db_session.commit()
            return obj
        except Exception as e:
            print("="*100)
            print("Exception")
            print(e)
            db_session.rollback()
            raise


    def list(self):
        """
        Lists all objects or the one specified by id.
        """
        return self.model.query.all()
        

    def search(self, **kwargs):
        """
        Searches for objects by the keyword arguments.
        """
        return self.model.query.filter_by(**kwargs)

    def delete(self, id):
        """
        Deletes objects by id.
        """
        obj = self.search(id=id)[0]
        db_session.delete(obj)
        try:
            db_session.commit()
            return obj
        except Exception as e:
            db_session.rollback()
            raise
        return obj



class CategoryController(BaseController):

    model = CategoryModel


class AdministratorController(BaseController):

    model = AdministratorModel


class SlideController(BaseController):

    model = SlideModel


category_controller = CategoryController()
administrator_controller = AdministratorController()
slide_controller = SlideController()