from database import db_session
from models import Administrator, Slide, Category
from flask import Flask, url_for, render_template, session, redirect, escape, request
app = Flask(__name__)


@app.route('/addCategory', methods=['GET', 'POST'])
def addCategory():
  cat = Category(request.form['name'])
  db_session.add(cat)
  db_session.commit()
  status = True
  categories = getCategories()
  return render_template('admin.html', categories = categories, status = status, action='added')

@app.route('/addSlide', methods=['GET', 'POST'])
def addSlide():

  screenshot = None
  s = Slide(request.form['title'], request.form['url'], request.form['description'], request.form['categorie'], screenshot)
  db_session.add(s)
  db_session.commit()

  categories = getCategories()
  status = True
  return render_template('admin.html', categories = categories, status = status, action='added')

@app.route('/deleteslide', methods=['GET', 'POST'])
def deleteSlide():
  slide_id = request.form['id']
  s = Slide.query.get(slide_id)
  db_session.delete(s)
  db_session.commit()
  status = True
  categories = getCategories()
  return render_template('admin.html', categories = categories, status = status, action='deleted')


@app.route('/updateslide', methods=['GET', 'POST'])
def updateSlide():
  slide_id = request.form['id']
  s = Slide.query.get(slide_id)
  s.title = request.form['title']
  s.description = request.form['description']
  s.url = request.form['url']
  s.category = request.form['categorie']
  db_session.add(s)
  db_session.commit()
  status = True
  categories = getCategories()
  return render_template('admin.html', categories = categories, status = status, action='updated')



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


# @app.route('/')
# def index():
#   categories = getCategories()
#   slides = getSlides()
#   return render_template('index.html', categories = categories, slides = slides)

@app.route('/')
def index():
  categories = getCategories()
  # slides = Slide.query.all()
  return render_template('index.html', categories = categories)

@app.route('/admin')
def admin():
  categories = getCategories()
  # return render_template('admin.html', categories = categories)
  # slides = getSlides()
  return render_template('admin.html', categories = categories)


@app.teardown_appcontext
def shutdown_session(exeception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
