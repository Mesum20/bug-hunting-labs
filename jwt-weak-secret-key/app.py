from flask import Flask, request, redirect, url_for, render_template, make_response, jsonify
import jwt
import datetime
import secrets

app = Flask(__name__)

# Secret key for JWT encoding/decoding (weak secret key for demonstration)
app.config['SECRET_KEY'] = '3nC0d3D$3cR3t'

# Simple in-memory storage for users
users = []
current_user = None

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'complexpassword123'  # Make it complex enough to be unbruteforcable

def create_jwt_token(username):
    payload = {
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def home():
    global current_user
    token = request.cookies.get('jwt')
    if token:
        payload = decode_jwt_token(token)
        if payload:
            return render_template('home.html', username=payload['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            token = create_jwt_token(username)
            resp = make_response(redirect(url_for('home')))
            resp.set_cookie('jwt', token)
            return resp
        for user in users:
            if user['username'] == username and user['password'] == password:
                token = create_jwt_token(username)
                resp = make_response(redirect(url_for('home')))
                resp.set_cookie('jwt', token)
                return resp
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if any(user['username'] == username for user in users):
            return 'Username already exists', 400
        users.append({'username': username, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin():
    global current_user
    token = request.cookies.get('jwt')
    if token:
        payload = decode_jwt_token(token)
        if payload and payload['username'] == ADMIN_USERNAME:
            return render_template('admin.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('jwt')
    return resp

if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5005)

