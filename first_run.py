import os

from database import init_db
from controllers import ( 
    category_controller, slide_controller,
    administrator_controller
)


if __name__ == '__main__':
   if not os.path.exists('db'):
      os.makedirs('db')
   print("Please open http://localhost:5000/init on your browser")

def init():
    init_db()
    
    print("Creating super admin")
    administrator_controller.create(
        nickname="", # add nickniame here
        email="", # add persona email
        active=True,
        super_admin=True
    )

    print("Createing the a test category..")
    category_controller.create(name="Test")
    category_controller.create(name="Uncategorised")
    print("Creating a test slide..")
    slide_controller.create(
        title="test title",
        screenshot="img/badge-reserved.jpg",
        description="test desc",
        url="https://github.com/moztn/firefoxOSAppDay-Slides",
        category=1,
        owner=1
    )
    print("Fixtures created successfully")
