import os
from database import init_db

if __name__ == '__main__':
  if not os.path.exists('db'):
    os.makedirs('db')
  init_db()


s = Slide(
	title="test title",
	screenshot="img/Pres-Mozilla.png",
	description="test desc",
	url="http://slides.mozilla-tunisia.org/demo/Pres-Mozilla",
	category=1
)

ss = Slide(
	title="test title 2",
	screenshot="img/Pres-Mozilla.png",
	description="test desc 2",
	url="http://moztn.github.io/firefoxOSAppDay-Slides",
	category=1
)


