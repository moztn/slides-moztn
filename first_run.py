import os

from database import init_db
from controllers import category_controller, slide_controller


if __name__ == '__main__':
    if not os.path.exists('db'):
        os.makedirs('db')
    init_db()
    
    print("Createing the a test category..")
    category_controller.create(name="Test")
    print("Creating a test slide..")
    slide_controller.create(
        title="test title",
        screenshot="img/Pres-Mozilla.png",
        description="test desc",
        url="http://moztn.github.io/firefoxOSAppDay-Slides",
        category=1
    )
    print("Fixtures created successfully")
