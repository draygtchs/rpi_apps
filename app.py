# Import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import logging

# Create an instance of the Flask class
app = Flask(__name__)

# Logging
app.logger.setLevel(logging.INFO) # Set the desired log level

def create_database():
    conn = sqlite3.connect('bucket_fillers.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fillers (id INTEGER PRIMARY KEY, filler TEXT)''')
    conn.commit()
    conn.close()

# Define a route and a function to handle requests to that route
@app.route('/')
def index():
	conn = sqlite3.connect('bucket_fillers.db')
	c = conn.cursor()
	c.execute('SELECT * FROM fillers')
	fillers = c.fetchall()
	conn.close()
	return render_template('index.html', fillers=fillers)

@app.route('/add', methods=['POST'])
def add_filler():
    filler = request.form['filler']
    conn = sqlite3.connect('bucket_fillers.db')
    c = conn.cursor()
    c.execute('INSERT INTO fillers (filler) VALUES (?)', (filler,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:filler_id>')
def delete_filler(filler_id):
    conn = sqlite3.connect('bucket_fillers.db')
    c = conn.cursor()
    c.execute('DELETE FROM fillers WHERE id = ?', (filler_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/entry', methods=['GET'])
def entry():
    return render_template('entry.html')

@app.route('/delete', methods=['GET'])
def delete():
    conn = sqlite3.connect('bucket_fillers.db')
    c = conn.cursor()
    c.execute('SELECT * FROM fillers')
    fillers = c.fetchall()
    conn.close()
    return render_template('delete.html', fillers=fillers)

# Run the application
if __name__ == '__main__':
	create_database()
	app.run(host='10.0.0.251')
