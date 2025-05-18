from flask import Flask, render_template, redirect, url_for, session, request
import sqlite3
import pandas
app = Flask(__name__)

def users():
    connection = sqlite3.connect("input.db")
    cursor = connection.cursor()
    #cursor.execute("DROP TABLE IF EXISTS input;")
    cursor.execute("""
CREATE table if NOT exists input(
	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	username TEXT,
	password TEXT);
""")
    df_input = pandas.read_sql_query("SELECT * FROM input;", connection)
    print(df_input)
    connection.commit()
    connection.close()
@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect("input.db")
        cursor = connection.cursor()
        #cursor.execute("DROP TABLE IF EXISTS input;")
        cursor.execute("""
        SELECT * FROM input WHERE USER = ? AND PASSWORD = ?
""",(name, password))
        user = cursor.fetchone()
        df_input = pandas.read_sql_query("SELECT * FROM input;", connection)
        print(df_input)
        connection.close()
        if user:
            session['user'] = name
            return redirect('/')
        else:
            return render_template('login.html', error ='invalid login')
    return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        try:
            connection = sqlite3.connect("input.db")
            cursor = connection.cursor()
            #cursor.execute("DROP TABLE IF EXISTS input;")
            cursor.execute("""
        INSERT INTO input (username, password) VALUES(?,?)
""",(name, password))
            return redirect('/')
        except sqlite3.IntegrityError: 
            return render_template('register.html', error ='username_exists')
    return render_template('register.html')


if __name__ == '__main__':
    users()
    app.run(debug=True)

