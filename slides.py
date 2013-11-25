from database import db_session
from models import Administrator, Slide, Category
from flask import Flask, url_for, render_template, request, redirect, abort
app = Flask(__name__)


def addCategory(name):
  cat = Category(name)
  db_session.add(cat)
  db_session.commit()

def addSlide(title, url, description, category, screenshot=None):
  s = Slide(title, url, description, category, screenshot)
  db_session.add(s)
  db_session.commit()

def addSlideFromForm(request):
  title = None
  url = None
  description = None
  category = None
  screenshot = None
  if 'title' in request.form:
    title = request.form['title']
  if 'url' in request.form:
    url = request.form['url']
  if 'description' in request.form:
    description = request.form['description']
  if 'category' in request.form:
    category = request.form['category']
  if 'screenshot' in request.form:
    screenshot = request.form['screenshot']
  if None in [title, url, description, category]:
    abort(400, "Incomplete form !")
    return
  addSlide(title, url, description, category, screenshot)

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
  if request.method == 'POST':
    addSlideFromForm(request)
  categories = getCategories()
  return render_template('admin.html', categories = categories)

@app.teardown_appcontext
def shutdown_session(exeception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
