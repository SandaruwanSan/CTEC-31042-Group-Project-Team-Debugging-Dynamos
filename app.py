from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create the users table
def create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Function to insert a user into the database
def add_user(username, password):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# for testing purpose
create_table()
add_user('st', '123')

# Route for the login page
@app.route('/')
def login():
    return render_template('login.html')

# Route to handle login form submission
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    
    # Check if the username and password match
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('welcome'))  # Redirect to the welcome page
    else:
        return 'Invalid username or password.'

# Route for the welcome page
@app.route('/welcome')
def welcome():
    return render_template('Welcome.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
