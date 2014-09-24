from database import db_session
from models import Administrator, Slide, Category
from flask import Flask, url_for, render_template, session, redirect, escape, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

app = Flask(__name__)


@app.route('/addCategory', methods=['GET', 'POST'])
def addCategory():
  category = Category(request.form['name'])
  try:
    Category.query.filter_by(name=request.form['name']).one()
    status = False 
  except NoResultFound:  
    db_session.add(category)
    db_session.commit()
    status = True
  return render_template('admin.html', status = status, action='added',operation='categories',message='This category already exists in DB!')



@app.route('/addSlide', methods=['GET', 'POST'])
def addSlide():
  try:
    status = 1
    categories = getCategories()
    message = isValidURL(request.form['url'])
    if(message != None):
      return render_template('admin.html', categories = categories, status = status, message = message)
    screenshot = None
    s = Slide(request.form['title'], request.form['url'], request.form['description'], request.form['categorie'], screenshot)
    db_session.add(s)
    db_session.commit()
    status = 0
    return render_template('admin.html', categories = categories, status = status, action='added')
  except IntegrityError as e:
    db_session.rollback()
    return render_template('admin.html', categories = categories, status = status, message ='This slide already exists')
    
    
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
  categories = getCategories()

  s.title = request.form['title']
  s.description = request.form['description']
  
  #check if URL added is correct
  message = isValidURL(request.form['url'])
  if(message==None):
    s.url = request.form['url']
    s.category = request.form['categorie']
    db_session.add(s)
    db_session.commit()
    status = True
  else:
    status = False    
  return render_template('admin.html', categories = categories, status = status, action='updated', message=message)



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

def isValidURL(url):
  
  # Check if the presentation is hosted on github
  if(url.lower().startswith('https://github.com/') is not True):
    return "Your slides must be hosted on https://github.com/"

  # Check if the branch 'gh-pages' exists
  import requests
  res = requests.get(url+'/tree/gh-pages')
  
  if(not res.ok):
    return "You have to create a 'gh-pages' branch"

  return None

@app.route('/')
def index():
  categories = getCategories()
  return render_template('index.html', categories = categories)

@app.route('/admin')
def admin():
  categories = getCategories()
  status = -1
  return render_template('admin.html', categories = categories, status = status)


@app.teardown_appcontext
def shutdown_session(exeception=None):
  db_session.remove()

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
