# Here we will define the database model
from . import db # here . represents the website package, we are accessing everthing inside the package only
from flask_login import UserMixin # module that helps log users in
from sqlalchemy.sql import func

class Note(db.Model): # Databas emdoel is a layour or a blueprint of the objects that will be stored in the database
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True), default = func.now()) # Func just gets the current data and time and use that to stoe in the timefield
    userId = db.Column(db.Integer, db.ForeignKey('user.id')) # this is the child node that refernce the User id[In python we Capitalise the Class but in sql it is represented as 'user'
    

class User(db.Model, UserMixin): # All the users have to conform to this model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') # Everytime we create a note db creates a relationship between the user and the notes objects





