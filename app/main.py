from app.db import Userg
from os import stat
from flask import Flask, json, render_template, request, jsonify, url_for, redirect, current_app
from firebase_admin import firestore, credentials, initialize_app
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super secret string"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    if not flask_login.current_user.is_authenticated:
        return render_template('index/index.html')
    else:
        userctx = Userg()
        userName = userctx.getItem(flask_login.current_user.id)
        fullname = userctx.fullname
        return render_template('index/index.html', user={'username':flask_login.current_user.id, 'name':fullname})

@app.route('/login', methods=['POST'])
def login():
    userctx = Userg()
    # from app.db import user
    content = request.get_json()
    if (content):
        username = str(content['username']).upper()
        password = content['password']
    else:
        username = (request.form['username']).upper()
        password = request.form['password']
    userName = userctx.getItem((content['username']).upper())
    passwordCheck = check_password_hash(userctx.password, password)
    if userName and passwordCheck:
        username = username
        name = userctx.fullname
        user = User()
        user.id = username
        flask_login.login_user(user)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})

# @login_manager.unauthorized_handler
# def unauthorized():
#     return "You're not allowed to login"

# @app.route('/user')
# @flask_login.login_required
# def user():
#     from app.db import user
#     userctx = user()
#     userName = userctx.getItem(flask_login.current_user.id)
#     fullname = userctx.fullname
#     return render_template('index/index.html', user={'username':flask_login.current_user.id, 'name':fullname})

@app.route('/logout', methods=['POST'])
def logout():
    flask_login.logout_user()
    return render_template('index/index.html')


@app.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    fullname = str(content['fullname'])
    username = str(content['username']).upper()
    password = str(content['password'])
    passwordHash = generate_password_hash(password, 'sha256')
    if (len(fullname) != 0 or len(username) != 0 or len(password) != 0):
        userCreate = Userg()
        userCreate.save(fullname, username, passwordHash)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})


@app.route('/test', methods=['GET', 'POST'])
def test():
    data = request.get_json()
    print(data)
