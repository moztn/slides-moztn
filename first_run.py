import os
from database import init_db

if __name__ == '__main__':
  if os.path.exists('db'):
    os.path.makedirs('db')
  init_db()


