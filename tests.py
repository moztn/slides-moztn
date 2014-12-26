import os
import config
import slides
import unittest
import tempfile
import database
from flask.ext.login import login_user , logout_user
from models import CategoryModel,AdministratorModel,SlideModel

@slides.app.route('/test_login')
def test_login():
    database.db_session.add(AdministratorModel("test"))
    database.db_session.commit()
    user = ( AdministratorModel.query.filter(AdministratorModel.email=="test").first())
    login_user(user)
    return "ok"

class SlidesTestCase(unittest.TestCase):

    def setUp(self):
        slides.app.config['TESTING'] = True
        self.app = slides.app.test_client()
        database.init_db()

    def tearDown(self):
        os.unlink("." + config.DATABASE)

    def test_index(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_add_new_category(self):
        rv = self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)
        assert "Category added succefully" in rv.data

    def test_only_logged_users_can_add_new_category(self):
        rv = self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)
        assert 'Unauthorized' in rv.data

    def test_add_existing_category(self):
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        rv = self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)
        assert "This Categorie already exists !" in rv.data

    def test_update_category(self):
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        rv = self.app.post('/updatecategory', data=dict(
             id=c.id, title="test2"), follow_redirects=True)
        assert "Category updated succefully" in rv.data

    def test_only_logged_users_can_update_category(self):
        self.app.get("/test_login")

        self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        self.app.post("/api/logout")

        rv = self.app.post('/updatecategory', data=dict(
             id=c.id, title="test2"), follow_redirects=True)
        assert 'Unauthorized' in rv.data

    @unittest.expectedFailure
    def test_update_category_with_existing_name(self):


        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        self.app.post('/addCategory', data=dict(
             name='test2'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test2").first()

        rv = self.app.post('/updatecategory', data=dict(
             id=c.id, title="test"), follow_redirects=True)
        assert "Category updated succefully" in rv.data

    def test_update_uncategorised_category(self):

        self.app.get('/init')

        c = CategoryModel.query.filter(CategoryModel.name=="Uncategorised").first()

        rv = self.app.post('/updatecategory', data=dict(
             id=c.id, name="test"), follow_redirects=True)
        assert "You can&#39;t change the name of this category" in rv.data


    def test_delete_category(self):
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        rv = self.app.post('/deletecategory', data=dict(
             id=c.id), follow_redirects=True)
        assert "Category deleted succefully" in rv.data

    def test_only_logged_users_can_delete_category(self):
        self.app.get("/test_login")

        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        self.app.post("/api/logout")

        rv = self.app.post('/deletecategory', data=dict(
             id=c.id), follow_redirects=True)
        assert 'Unauthorized' in rv.data

    def test_delete_uncategorised_category(self):
        self.app.get('/init')

        c = CategoryModel.query.filter(CategoryModel.name=="Uncategorised").first()

        rv = self.app.post('/deletecategory', data=dict(
             id=c.id, name="test"), follow_redirects=True)
        assert "You can&#39;t delete this category" in rv.data


    @unittest.expectedFailure
    def test_add_new_slide_with_valid_url(self):
        self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        rv = self.app.post('/addSlide', data=dict(
            title='Firefox OS App Day Tunisia',
            url='https://github.com/moztn/firefoxOSAppDay-Slides',
            description='Firefox OS App Day Tunisia Event',
            categorie=c.id)
          )

        print rv.data

        assert "Slide added succefully" in rv.data

    def test_add_new_slide_with_non_github_url(self):
        self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        rv = self.app.post('/addSlide', data=dict(
            title='Firefox OS App Day Tunisia',
            url='https://www.mozilla-tunisia.org/moztn/firefoxOSAppDay-Slides',
            description='Firefox OS App Day Tunisia Event',
            categorie=c.id)
          )

        assert "Your slides must be hosted on https://github.com/" in rv.data

    @unittest.expectedFailure
    def test_add_new_slide_with_non_gh_pages_branch(self):
        self.app.post('/addCategory', data=dict(
              name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        rv = self.app.post('/addSlide', data=dict(
            title='Firefox OS App Day Tunisia',
            url='https://github.com/moztn/moztnbot',
            description='Firefox OS App Day Tunisia Event',
            categorie=c.id)
          )

        assert "You have to create a 'gh-pages' branch" in rv.data

    def test_only_logged_users_can_add_slide(self):
        self.app.get("/test_login")
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        self.app.post("/api/logout")

        rv = self.app.post('/addSlide', data=dict(
           title='Firefox OS App Day Tunisia',
           url='https://github.com/moztn/firefoxOSAppDay-Slides',
           description='Firefox OS App Day Tunisia Event',
           categorie=c.id)
         )
        assert 'Unauthorized' in rv.data

    def test_only_logged_users_can_update_slide(self):
        self.app.get("/test_login")
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        self.app.post('/addSlide', data=dict(
           title='Firefox OS App Day Tunisia',
           url='https://github.com/moztn/firefoxOSAppDay-Slides',
           description='Firefox OS App Day Tunisia Event',
           screenshot = "img/badge-reserved.jpg",
           categorie=c.name)
         )

        s = SlideModel.query.filter(SlideModel.title=='Firefox OS App Day Tunisia').first()

        self.app.post("/api/logout")

        rv=self.app.post('/addSlide', data=dict(
           id=s.id,
           title='Firefox OS App Day TN',
           url=s.url,
           description=s.description,
           screenshot = s.screenshot,
           categorie=s.category)
         )

        assert 'Unauthorized' in rv.data

    def test_only_logged_users_can_delete_slide(self):
        self.app.get("/test_login")
        self.app.post('/addCategory', data=dict(
            name='test'), follow_redirects=True)

        c = CategoryModel.query.filter(CategoryModel.name=="test").first()

        self.app.post('/addSlide', data=dict(
          title='Firefox OS App Day Tunisia',
          url='https://github.com/moztn/firefoxOSAppDay-Slides',
          description='Firefox OS App Day Tunisia Event',
          screenshot = "img/badge-reserved.jpg",
          categorie=c.name)
         )

        s = SlideModel.query.filter(SlideModel.title=='Firefox OS App Day Tunisia').first()

        self.app.post("/api/logout")

        rv=self.app.post('/deleteslide', data=dict(
           id=s.id)
           )

        assert 'Unauthorized' in rv.data

    def test_access_to_admin_page_denied_if_not_logged_in(self):
       rv = self.app.get('/admin')
       assert 'You must be logged in to access this page' in rv.data




if __name__ == '__main__':
    unittest.main(verbosity=2)
