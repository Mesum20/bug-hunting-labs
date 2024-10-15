from flask import Flask, render_template, request, redirect, make_response
import jwt

app = Flask(__name__)
app.secret_key = 'mynameissomethingyoucantguess'

# In-memory user list (username, password)
users = [
    {"username": "admin", "password": "SuperComplexPass123!"},
]

# JWT secret key (for signature)
JWT_SECRET = 'thisisaverysecretkey'

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple in-memory check
        for user in users:
            if user['username'] == username and user['password'] == password:
                token = jwt.encode({"username": username}, JWT_SECRET, algorithm="HS256")
                resp = make_response(redirect('/dashboard'))
                resp.set_cookie('jwt', token)
                return resp
        return "Invalid credentials!", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add user to the list
        users.append({"username": username, "password": password})
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('jwt')
    if not token:
        return redirect('/login')

    try:
        # Decode JWT without signature verification to demonstrate the flaw
        decoded = jwt.decode(token, options={"verify_signature": False})
        username = decoded['username']
        
        # Admin user flag display
        if username == 'admin':
            flag = "flag{jwt_m4st3r_y0u_b34t_th3_t0k3n}"
        else:
            flag = None
        return render_template('dashboard.html', username=username, flag=flag)
    
    except jwt.ExpiredSignatureError:
        return 'Token has expired!', 403
    except Exception as e:
        return 'Invalid token!', 403

@app.route('/logout')
def logout():
    resp = make_response(redirect('/login'))
    resp.set_cookie('jwt', '', expires=0)
    return resp

if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5003)

