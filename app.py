import subprocess
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

vuln_pages = [
    {"title": "OS Command injection", "link": "/os"}
]

@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username, vuln_pages=vuln_pages)
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            con = sqlite3.connect('ciel.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
            result = cur.fetchall()
            con.close()

            if result:
                if password == result[0][1]:
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    error = f"Wrong password for {result[0][0]}"
                    return render_template('login.html', error=error)
            else:
                error = "Couldn't find that user"
                return render_template('login.html', error=error)
        except Exception as e:
            raise e
    else:
        return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        try:
            con = sqlite3.connect('ciel.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username = '%s'" % username)
            result = cur.fetchall()

            if result:
                error = f"User {result[0][0]} already exists"
                return render_template('register.html', error=error)
            else:
                cur.execute("INSERT INTO users VALUES ('%s', '%s')" % (username, password))
                con.commit()
                con.close()
                return redirect(url_for('login'))
        except Exception as e:
            raise e
    else:
        return render_template('register.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/os", methods=["GET", "POST"])
def os():
    if 'username' in session:
        username = session['username']
        if request.method == "POST":
            command = request.form['command'].split()
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            command = ' '.join(command)
            return render_template('os.html', command=command, result=result.stdout, username=username)
        else:
            return render_template('os.html', username=username)
    else:
        return redirect(url_for('index'))
