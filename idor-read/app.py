from flask import Flask, request, redirect, url_for, render_template, session, jsonify
import uuid
import json

app = Flask(__name__)
app.secret_key = 'mynameissomethingyoucantguess'

# Load user data from a JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

# Home Route
@app.route('/')
def index():
    return redirect(url_for('login'))

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            return 'User already exists!'

        user_id = str(uuid.uuid4())
        users[username] = {'password': password, 'id': user_id, 'posts': []}
        save_users(users)
        return redirect(url_for('login'))

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('upload_post'))

        return 'Invalid credentials!'

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Upload Post
@app.route('/upload_post', methods=['GET', 'POST'])
def upload_post():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        post_content = request.form['post']
        users = load_users()
        user = session['username']

        users[user]['posts'].append({'id': str(uuid.uuid4()), 'content': post_content})
        save_users(users)
        return redirect(url_for('view_posts'))

    return render_template('upload_post.html')

# View Posts by User
@app.route('/view_posts')
def view_posts():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    user = session['username']
    user_posts = users[user]['posts']

    return render_template('view_posts.html', posts=user_posts)

# View Post by ID (IDOR vulnerability)
@app.route('/post/<post_id>')
def view_post(post_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    for user, data in users.items():
        for post in data['posts']:
            if post['id'] == post_id:
                return render_template('view_post.html', post=post)

    return 'Post not found!'

# User UUIDs and Post UUIDs (For demonstration only)
@app.route('/user')
def user_uuids():
    if 'username' not in session:
        return redirect(url_for('login'))

    users = load_users()
    uuid_list = {}
    for user, data in users.items():
        uuid_list[user] = {
            'user_uuid': data['id'],
            'posts': {post['id']: None for post in data['posts']}  # Show only post UUIDs
        }

    return jsonify(uuid_list)

if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5001)

