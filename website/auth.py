from flask import Blueprint,flash, redirect, render_template, url_for, request
import hashlib
from werkzeug.security import generate_password_hash,check_password_hash
from .models import Account
from . import db
from flask_login import login_user, login_required , current_user, logout_user

auth = Blueprint('auth',__name__)

def genarate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

@auth.route(f'/about/{genarate_hash("about")}')
@login_required
def about():
    return render_template('about.html', user = current_user)

@auth.route(f'/service/{genarate_hash("service")}')
@login_required
def service():
    return render_template('service.html', user = current_user)

@auth.route(f'/team/{genarate_hash("team")}')
@login_required
def team():
    return render_template('team.html', user = current_user)

@auth.route(f'/why/{genarate_hash("why")}')
@login_required
def why():
    return render_template('why.html', user = current_user)

@auth.route(f'/main/{genarate_hash("main")}')
@login_required
def main():
    return render_template('index.html', user = current_user)

@auth.route('/logout')
@login_required
def logout():
    current_user = None
    logout_user()
    return redirect(url_for('auth.login', user = current_user))

@auth.route('/login', methods=['POST','GET'])
def login():
    current_user = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash("Please fill out all fieds", category='error')
            return redirect(url_for('auth.login', user = current_user))
        
        user = Account.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Login successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.main',user = current_user))
        else:
            flash("Email is not exists!", category='error')
    return render_template('login.html', user = current_user)

@auth.route('/signup',methods = ['GET','POST'])
def signup():
    current_user = None
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if not email or not password1 or not password2:
            flash("Please fill out all fieds", category='error')
            return redirect(url_for('auth.signup', user = current_user))
        
        user = Account.query.filter_by(email = email).first()
        if user:
            flash("Email already exists", category='error')
        else:
            if(password1!=password2):
                flash("Confirm password incorrect", category='error')
                return redirect(url_for('auth.signup', user = current_user))
            else:
                new_user = Account(email = email, password = generate_password_hash(password1))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash("Accout created", category='success')
                return redirect(url_for('auth.login'))
    return render_template('signup.html', user = current_user)