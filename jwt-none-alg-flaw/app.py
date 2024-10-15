from flask import Flask, request, jsonify, redirect, url_for, render_template, make_response
import jwt
import datetime
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mynameissomethingyoucantguess'  # Change this to a secure key

# List-based storage for users
users = [
    {'username': 'admin', 'password': 'ComplexP@ssw0rd', 'is_admin': True}
]

def create_jwt(username, is_admin=False):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'username': username,
        'exp': expiration,
        'is_admin': is_admin
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def verify_jwt(token):
    try:
        # Decode JWT without verifying signature if 'none' algorithm is used
        header = jwt.get_unverified_header(token)
        if header['alg'] == 'none':
            # Decode without verifying signature
            payload = jwt.decode(token, options={"verify_signature": False})
        else:
            # Verify with the correct key and algorithm
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt')
        if not token or not verify_jwt(token):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def dashboard():
    token = request.cookies.get('jwt')
    payload = verify_jwt(token)
    if payload and payload['is_admin']:
        return render_template('dashboard.html', flag='flag{jwt_n0ne_alg0r1thm_4tt4ck}')
    return "Welcome, {}!".format(payload['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u['username'] == username), None)
        if user and user['password'] == password:
            token = create_jwt(username, user.get('is_admin', False))
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('jwt', token)
            return resp
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not any(u['username'] == username for u in users):
            users.append({'username': username, 'password': password, 'is_admin': False})
            return redirect(url_for('login'))
        return 'User already exists', 400
    return render_template('register.html')

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('jwt', '', expires=0)
    return resp

if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5004)

