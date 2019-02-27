from flask import render_template, flash, redirect, url_for, request, render_template_string
from flask_login import login_user, current_user, logout_user
from app import app,db
from app.models import User
from app.forms import RegisterForm, LoginForm

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                 password_hash=User.set_password(form.password.data),
                 email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('user'))
    return render_template('login.html', form = form)

@app.route('/user')
def user():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.id == 1:
        return render_template('admin.html')
    return render_template('user.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
@app.errorhandler(404)
def page_not_found(error):
    path = request.path
    path = path.replace('(','')
    path = path.replace(')','')
    template = '''
{%% extends "base.html" %%}
{%% block content %%}
<div style="text-align: center;font-size: 30px;">
    <div>
        <p class="alert alert-info">
            %s doesn't exist.
        </p>
    </div>
</div>
{%% endblock %%}
''' % (path)
    return render_template_string(template),404