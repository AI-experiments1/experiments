from urllib.parse import urlsplit
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter(db.func.lower(User.email) == email).first():
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))
        user = User(name=form.name.data, email=email, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter(db.func.lower(User.email) == email).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            # Only allow relative redirects to prevent open-redirect attacks
            if not next_page or '\\' in next_page or not next_page.startswith('/') \
                    or next_page.startswith('//') or urlsplit(next_page).netloc:
                next_page = url_for('main.index')
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(next_page)
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')
