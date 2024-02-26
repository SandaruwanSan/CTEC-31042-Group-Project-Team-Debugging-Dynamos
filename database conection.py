from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# create the database(if it is not exist)
def create_table():
    conn = sqlite3.connect('internships.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS internships 
                 (company text, position text, duration text)''')
    conn.commit()
    conn.close()

# adding internship to the database
def insert_internship(company, position, duration):
    conn = sqlite3.connect('internships.db')
    c = conn.cursor()
    c.execute("INSERT INTO internships VALUES (?, ?, ?)", (company, position, duration))
    conn.commit()
    conn.close()

# retriveve all internship data from database
def get_internships():
    conn = sqlite3.connect('internships.db')
    c = conn.cursor()
    c.execute("SELECT * FROM internships")
    internships = c.fetchall()
    conn.close()
    return internships

#creatin  table for database
create_table()

# linked to the home page
@app.route('/')
def home():
    internships = get_internships()
    return render_template('index.html', internships=internships)

# linked into internship form page
@app.route('/add_internship', methods=['GET', 'POST'])
def add_internship():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        duration = request.form['duration']
        insert_internship(company, position, duration)
        return render_template('success.html', company=company, position=position)
    return render_template('add_internship.html')

if __name__ == '__main__':
    app.run(debug=True)
#end of the python backend part for adding internship












 
