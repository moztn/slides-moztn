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



if __name__ == '__main__':
    unittest.main()
