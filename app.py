from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret'

def init_db():
    conn = sqlite3.connect('input.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pw = request.form['password']

        conn = sqlite3.connect('input.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (name, pw))
        user = cur.fetchone()
        conn.close()

        if user:
            session['user'] = name
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid login")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        pw1 = request.form['password']
        pw2 = request.form['confirm']

        if pw1 != pw2:
            return render_template('register.html', error="Passwords do not match")

        try:
            conn = sqlite3.connect('input.db')
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, pw1))
            conn.commit()
            conn.close()
            session['user'] = name
            return redirect('/')
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Username exists")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)