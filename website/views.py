from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .model import Note
from . import db
import json
#current user has a bunch of attributes. if the user is logged in, it gives us a bunch of information about the user like its name, notes,emails
#if the user is not, then it will tell the user is anonymous and right now not authenticated


#This file is the blueprint of our application which simply means that it has a bunch of roots and url defined inside of it
#This is a way to seperate our app out so we dont have all the views defined in one file and we can have to spread out neatly and organised.

views = Blueprint('views',__name__)

#This function will run whenever we go to the / This is a decorator.
@views.route('/',methods = ['GET','POST'])
@login_required # now we cannot reach the home page until you login
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note,userId=current_user.id) #creating a new obejct of the class Note for the current_user.
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user = current_user) # useing the user, in our template we can if the user exists and authenticated

@views.route('/delete-note',methods=['POST'])
def delete_node():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.userId == current_user.id: # We can only delete our own notes. We should not be allowed to delete other people notes
            db.session.delete(note)
            db.session.commit()
    return jsonify({}) # returning an empty result
