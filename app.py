from os import stat
from flask import Flask, json, render_template, request, jsonify, url_for, redirect
import flask_login

app = Flask(__name__)
app.secret_key = "super secret string"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'devamanin': {'name': 'Aman',
                       'password': 'aman1', 'email': 'aman@gmail.com'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    user = {'username': 'devamanin', 'name': 'Aman'}
    return render_template('index/index.html',)


@app.route('/login', methods=['POST'])
def login():
    from db import user
    content = request.get_json()
    userctx = user()
    userName = userctx.getItem(content['username'])
    print(userName)
    if (content):
        username = content['username']
        password = content['password']
    else:
        username = request.form['username']
        password = request.form['password']
    # username = content['username']
    # password = content['password']
    # print(content['username'])
    # username = 'devamanin'
    # password = 'aman1'
    if username in users:
        if password == users[username]['password']:
            username = username
            name = users[username]['name']
            user = User()
            user.id = username
            flask_login.login_user(user)
            return jsonify({'status': 'success'})
            # return redirect(url_for('user'))
        else:
            return jsonify({'status': 'failed'})
    else:
        return jsonify({'status': 'failed'})
        # return render_template('index/user.html', user={'username': username, 'name': name})


@app.route('/user')
@flask_login.login_required
def user():
    return render_template('index/user.html', user={'username': flask_login.current_user.id, 'name': users[flask_login.current_user.id]['name']})


@app.route('/logout', methods=['POST'])
def logout():
    flask_login.logout_user()
    return render_template('index/index.html')


@app.route('/register', methods=['POST'])
def register():
    content = request.get_json()
    fullname = str(content['fullname'])
    username = str(content['username'])
    password = str(content['password'])
    # print(fullname, username, password)
    if (len(fullname) != 0 or len(username) != 0 or len(password) != 0):
        from db import user
        userCreate = user()
        userCreate.save(fullname, username, password)
        # setUser(fullname, username, password)
#         userCreate = user()
# userCreate.save('aman', 'devamanin', 'aman1')
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failed'})


@app.route('/test', methods=['GET', 'POST'])
def test():
    data = request.get_json()
    print(data)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
