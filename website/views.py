from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from .models import User,Note
from . import db

views = Blueprint('views',__name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/notes', methods=['GET','POST'])
@login_required
def notes():
    if request.method=='POST':
        title = request.form.get('title')
        data = request.form.get('data')

        if len(data)<1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(title=title,data=data,uder_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template('notes.html', user=current_user)

@views.route('/delete/<int:id>')
@login_required
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    flash('Note Deleted Successfully', category='success')
    return redirect(url_for('views.notes'))

@views.route("/update/<int:id>", methods = ['GET', 'POST'])
@login_required
def update(id):
    if(request.method=='POST'):
        title = request.form['title']
        data = request.form['data']
        note = Note.query.filter_by(id=id).first()
        note.title = title
        note.data = data
        db.session.add(note)
        db.session.commit()
        flash('Note Updated!', category='success')
        return redirect(url_for('views.notes'))

    return render_template('update.html', user=current_user)