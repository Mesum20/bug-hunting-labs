from flask import Flask, request, redirect, render_template, session, url_for
import uuid

app = Flask(__name__)
app.secret_key = 'mynameissomethingyoucantguess'

# In-memory data
users = {
    "user1": {"username": "user1", "password": "pass1", "uuid": str(uuid.uuid4())},
    "user2": {"username": "user2", "password": "pass2", "uuid": str(uuid.uuid4())},
}

posts = []  # Store posts as a list of dicts with uuid and content

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['uuid'] = users[username]['uuid']
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return "Username already exists. Please choose a different username.", 400
        if not username or not password:
            return "Username and password cannot be empty.", 400
        users[username] = {"username": username, "password": password, "uuid": str(uuid.uuid4())}
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_posts = [post for post in posts if post['uuid'] == session['uuid']]
    return render_template('dashboard.html', posts=user_posts)

@app.route('/create_post', methods=['POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('login'))
    content = request.form['content']
    posts.append({"uuid": session['uuid'], "content": content})
    return redirect(url_for('dashboard'))

@app.route('/delete_post/<post_uuid>', methods=['POST'])
def delete_post(post_uuid):
    global posts
    if 'user' not in session:
        return redirect(url_for('login'))
    posts = [post for post in posts if post['uuid'] != post_uuid]  # Vulnerable to IDOR
    return redirect(url_for('dashboard'))

@app.route('/id')
def id():
    # Leak all UUIDs (for IDOR demo)
    return {"users": {u['uuid']: u['username'] for u in users.values()}}
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('uuid', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5002)


