from flask import Flask, render_template, request, redirect, url_for, flash, abort, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'mynameissomethingyoucantguess'

# Predefined admin user
users = [
    {'username': 'admin', 'password': 'C0mpl3xP@ssw0rd!'}  # Hardcoded admin with complex password
]

# Admin flag
admin_flag = 'flag{fuzz1ng_d1scl0s3d_sens1t1ve_1nf0}'

# Define the path to the db directory
db_dir = os.path.join(os.getcwd(), 'db')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Check for admin user
    for user in users:
        if user['username'] == username and user['password'] == password:
            if username == 'admin':
                flash(f'Successfully logged in as admin! Here is your flag: {admin_flag}', 'success')
            else:
                flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
    
    flash('Invalid credentials, try again.', 'danger')
    return redirect(url_for('home'))

# Route for /db (returns 403 Forbidden)
@app.route('/db/')
@app.route('/db')
def forbidden_directory():
    return abort(403)

# Route for /db/backup.sql (allows downloading the file)
@app.route('/db/backup.sql')
def serve_backup_sql():
    try:
        return send_from_directory(db_dir, 'backup.sql', as_attachment=True)  # Forces download
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    # Change the host and port
    app.run(host='0.0.0.0', port=5000)


