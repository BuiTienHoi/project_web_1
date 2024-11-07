from flask import Blueprint, render_template ,flash, url_for, request, redirect
from .auth import genarate_hash
from flask_login import login_required, current_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Account
views = Blueprint('views',__name__)

@views.route('/', methods=['POST','GET'])
@login_required
def base():
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
                return redirect(url_for('auth.main',user = current_user,hsa = genarate_hash("home")))
        else:
            flash("Email is not exists!", category='error')
    return render_template('login.html', user = current_user)