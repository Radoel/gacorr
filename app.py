from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Untuk session

# Buat tabel di database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Halaman registrasi
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                      (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username sudah ada, coba yang lain!"

    return render_template('register.html')

# Halaman login
@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username  # Simpan username di session
            return redirect(url_for('dashboard'))  # Redirect ke dashboard
        else:
            return "Login gagal! Username atau password salah."

    return render_template('index.html')

# Halaman dashboard
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('index'))  # Kembali ke login kalau belum login

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Hapus session
    return redirect(url_for('index'))

# Halaman utama
@app.route('/')
def home():
    return "Selamat datang! Silakan <a href='/register'>daftar</a> atau <a href='/login'>login</a>."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)