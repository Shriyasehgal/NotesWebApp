from flask import Flask
from flask_sqlalchemy import SQLAlchemy # setting up our database
from os import path
from flask_login import LoginManager
db = SQLAlchemy() # We will use this when we need to add something to the database or create a new user.
DB_Name = 'database.db'

def create_app():
    app = Flask (__name__, template_folder='template')
    app.config['SECRET_KEY'] = 'joseihfknfhfg' #This will encrypt and the secure the cookies and the session data. ( THis is the secret key for the app)
    #Registering the blueprints in the init.py

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}' # this will store the database in the website folder.
    db.init_app(app) #this will take the databse that we design here and tell them that this app will be using the database

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .model import User, Note # this is done so we make sure that this User and Note file runs these blueprint classes before we create the databse

    login_manager = LoginManager() # this will help us manage all the logining in related things. 
    login_manager.login_view = 'auth.login' #Where do we go if we are not logged in, then we go to the login template
    login_manager.init_app(app) #telling the login manager which app we are using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/'+DB_Name): # Checking if the databse exists, if it doesnot we create it.
        db.create_all(app=app) 
        print('Created Databse!')