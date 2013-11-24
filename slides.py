from database import db_session
from models import Administrator, Slide, Category
from flask import Flask, url_for, render_template
app = Flask(__name__)


def addCategory(name):
  cat = Category(name)
  db_session.add(cat)
  db_session.commit()

def addSlide(title, url, description, category, screenshot=None):
  s = Slide(title, url, description, category, screenshot)
  db_session.add(s)
  db_session.commit()

# retrives the list of categories from the database
def getCategories():
  return Category.query.all()

# retrives slides for a given category
@app.template_filter('getSlides')
def getSlides(category):
  return Slide.query.filter(Slide.category == category.id)

def isAdmin(email):
  # if there is no result retrived from the administrator's table then
  # the mail is not administrator
  return (len(Administrator.query.filter(Administrator.email == email)) != 0)


@app.route('/')
def index():
  categories = getCategories()
  return render_template('index.html', categories = categories)

@app.route('/admin')
def admin():
  categories = getCategories()
  return render_template('admin.html', categories = categories)

@app.teardown_appcontext
def shutdown_session(exeception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run(host='0.0.0.0')
