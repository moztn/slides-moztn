from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from flask import (
    Flask, url_for, render_template, session, redirect, escape, request,
    flash, redirect, current_app
)

from database import db_session
from models import AdministratorModel, SlideModel, CategoryModel
from controllers import category_controller, slide_controller
from flask.ext.login import LoginManager
from flask.ext.browserid import BrowserID

def get_admin_by_id(aId):
  try:
    admin = AdministratorModel.query.get(int(aId))
    return admin
  except NoResultFound:
    return None

def get_admin(kwargs):
  try:
    admin = AdministratorModel.query.filter_by(email=kwargs['email']).first()
    return admin
  except NoResultFound:
    return None

app = Flask(__name__)

app.config['SECRET_KEY'] = "deterministic"

login_manager = LoginManager()
login_manager.user_loader(get_admin_by_id)
login_manager.init_app(app)
browser_id = BrowserID()
browser_id.user_loader(get_admin)
browser_id.redirect_url = 'admin'
browser_id.init_app(app)

@app.route('/init')
def first_run():
  import first_run
  first_run.init()
  return redirect(url_for("index"))

@app.route('/addCategory', methods=['GET', 'POST'])
def add_category():
    # categories = category_controller.list()
    # category = CategoryModel(request.form['name'])
    category_controller.create(
        name=request.form['name']
    )

    status = True
    return render_template(
        'admin.html',
        status=status,
        action='added',
        operation='categories',
        categories=category_controller.list(),
        message='This category already exists in DB!'
    )


@app.route('/addSlide', methods=['GET', 'POST'])
def add_slide():
    current_app.logger.debug("debug aaddSlide")
    message = isValidURL(request.form['url'])
    if message is not None:
        return render_template(
            'admin.html',
            categories=category_controller.list(),
            status=False,
            message=message
        )

    # Takes a default value in case screenshot not specified.
    if not request.form['screenshot']:
      screenshot = "img/badge-reserved.jpg"
    else:
      screenshot = request.form['screenshot']
    slide_controller.create(
        title=request.form['title'],
        url=request.form['url'],
        description=request.form['description'],
        category=request.form['categorie'],
        screenshot=screenshot,
    )
    redirect(url_for("admin"))

    return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=True,
        action='added'
    )
    # except IntegrityError as e:
    #     print("="*100)
    #     print("inter")
    #     db_session.rollback()
    #     raise
    # else:
    #     raise Exception("NOt i err")
    #     return render_template(
    #         'admin.html',
    #         categories=category_controller.list(),
    #         status=status,
    #         message='This slide already exists'
    #     )
    
    
@app.route('/deleteslide', methods=['GET', 'POST'])
def delete_slide():
    """
    Deletes a slide.
    """
    slide_controller.delete(request.form['id'])

    return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=True,
        action='deleted'
    )

@app.route('/deletecategory', methods=['GET', 'POST'])
def delete_category():
    """
    Deletes a category.
    """
    category_id = request.form['id']
    c = CategoryModel.query.get(category_id)

    uc = CategoryModel.query.filter(CategoryModel.name=="Uncategorised").first()
    if uc is None:
        category_controller.create(
        name="Uncategorised"
    )

    if c.name == "Uncategorised":
        return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=False,
        action='deleted',
        operation='categories',
        message="You can't delete this category"
        )


    slides = get_slides_by_cotegory(c)
    for s in slides:
        s.category = uc.id
        db_session.add(s)
    category_controller.delete(category_id)
    
    db_session.commit()


    return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=True,
        action='deleted',
        operation='categories'
    )


@app.route('/updateslide', methods=['GET', 'POST'])
def update_slide():
    """
    Updates a slide.
    """
    current_app.logger.debug("debug updateSlide")
    message = isValidURL(request.form['url'])
    if message is not None:
        return render_template(
            'admin.html',
            categories=category_controller.list(),
            status=False,
            message=message
        )
    if not request.form['screenshot']:
      screenshot = "img/badge-reserved.jpg"
    else:
      screenshot = request.form['screenshot']
    slide_id = request.form['id']
    s = SlideModel.query.get(slide_id)
    s.title = request.form['title']
    s.description = request.form['description']
    s.url = request.form['url']
    s.category = request.form['categorie']
    s.screenshot = screenshot
    db_session.add(s)
    db_session.commit()
    status = True

    return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=status,
        action='updated'
    )

@app.route('/updatecategory', methods=['GET', 'POST'])
def update_category():
    """
    Updates a category.
    """

    category_id = request.form['id']
    c = CategoryModel.query.get(category_id)
 
    if c.name == "Uncategorised":
        return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=False,
        action='updated',
        operation='categories',
        message="You can't change the name of this category"
        )

    c.name = request.form['title']
   
    db_session.add(c)
    db_session.commit()
    status = True

    return render_template(
        'admin.html',
        categories=category_controller.list(),
        status=status,
        action='updated',
        operation='categories'
    )

# retrives slides for a given category
@app.template_filter('getSlides')
def get_slides_by_cotegory(category):
    """
    """
    return slide_controller.search(category=category.id)

# def isAdmin(email):
#   # if there is no result retrived from the administrator's table then
#   # the mail is not administrator
#   return (len(AdministratorModel.query.filter(AdministratorModel.email == email)) != 0)

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
    """
    Returns the index view.
    """
    return render_template(
        'index.html',
        categories=category_controller.list()
    )

@app.route('/admin')
def admin():
    current_app.logger.debug("debug admin")
    status = -1
    return render_template(
    'admin.html',
    categories=category_controller.list(),
    status=status
)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.before_request
def log_entry():
    context = {
        'url': request.path,
        'method': request.method,
        'ip': request.environ.get("REMOTE_ADDR")
    }
    app.logger.debug("Handling %(method)s request from %(ip)s for %(url)s", context)

@app.teardown_appcontext
def shutdown_session(exeception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, use_debugger=True)
