from flask import Blueprint, render_template, request, flash, url_for, redirect
import re
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
  
def ValidEmail(email):   
    if(re.search(regex,email)):   
        return True
       
    return False

def password_check(passwd):
    SpecialSym =['$', '@', '#', '%']
    val = True
      
    if len(passwd) < 8:
        val = False
    if len(passwd) > 20:
        val = False          
    if not any(char.isdigit() for char in passwd):
        val = False          
    if not any(char.isupper() for char in passwd):
        val = False          
    if not any(char.islower() for char in passwd):
        val = False          
    if not any(char in SpecialSym for char in passwd):
        val = False
    
    return val

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user :
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template('login.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user :
            flash("Entered email already exist", category='error')
        elif ValidEmail(email)==False:
            flash("Entered Email is not Valid", category='error')
        elif len(first_name)<3:
            flash("Firstname should be greater than 2 characters", category='error')
        elif password_check(password1)==False:
            flash(" Password length should be >=8 but <=20. Password should contain one numeral, one uppercase letter, one lowercase letter and one special symbol.",category='error')
        elif len(password1)!=len(password2):
            flash("Passwords don't match.",category='error')
        else:
            new_user = User(email=email, first_name=first_name,last_name=last_name,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account Created!",category='success')
            return redirect(url_for('views.home'))


    return render_template('signup.html', user=current_user)