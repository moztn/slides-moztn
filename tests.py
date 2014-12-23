import os
import config
import slides
import unittest
import tempfile
import database



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

    def test_add_existing_category(self):
        self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)

        rv = self.app.post('/addCategory', data=dict(
             name='test'), follow_redirects=True)
        assert "This Categorie already exists !" in rv.data





if __name__ == '__main__':
    unittest.main()
