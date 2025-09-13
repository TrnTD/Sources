from flask import Flask, request, render_template, redirect, url_for, flash, make_response
import sqlite3
from auth import generate_token, verify_token, login_required

app = Flask(__name__)
app.secret_key = "supersecret_nooneknow"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
	return render_template('login_signup.html')


@app.route('/register', methods=['POST'])
def register():
	username = request.form.get('username')
	password = request.form.get('password')

	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	try:
		c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))

		conn.commit()
		flash("Đăng ký thành công! Hãy đăng nhập.")

	except sqlite3.IntegrityError:
		flash("Username đã tồn tại!")
	conn.close()

	return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
	username = request.form.get('username')
	password = request.form.get('password')
	role = request.form.get('role', 'guest')

	conn = sqlite3.connect("users.db")
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
	user = c.fetchone()
	conn.close()

	if user:
		token = generate_token(username, role)
		response = make_response(redirect(url_for('dashboard')))
		response.set_cookie("jwt_token", token, httponly=True, samesite="Lax", max_age=3600)

		return response

	return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
	return render_template("dashboard.html")


@app.route('/flag')
@login_required
def flag():
	token = request.cookies.get('jwt_token')
	data = verify_token(token)
	role = data['role']
	if role == 'admin':
		return "CONGRATS, HERE IS YOUR FLAG: PTITHCM{4cc3ss_c0ntr0l_vuln3r4b1l1ty}"
	else:
		return "Sorry no FLAG for you! You're not admin!"


@app.route('/logout')
@login_required
def logout():
	response = make_response(redirect(url_for("index")))
	response.delete_cookie("jwt_token")
	return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9002)