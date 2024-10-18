from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

# Function to encrypt password using SHA-256
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Home/Sign-up route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        middle_name = request.form.get('midname')
        last_name = request.form.get('last_name')
        age = request.form.get('age')
        email = request.form.get('email')
        contact = request.form.get('contact')
        address = request.form.get('address')
        password = request.form.get('password')

        # Encrypt password
        encrypted_password = encrypt_password(password)

        # Insert user data into MySQL database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (name, middle_name, last_name, age, email, contact, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, middle_name, last_name, age, email, contact, address, encrypted_password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('login'))

    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            encrypted_password = encrypt_password(password)
            if user[8] == encrypted_password: 
                session['logged_in'] = True
                session['name'] = user[1] 
                session['user_id'] = user[0] 
                return redirect(url_for('dashboard'))
            else:
                return "Invalid username or password"
        else:
            return "Invalid username or password"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, middle_name, last_name, age, email, contact, address FROM users WHERE id=%s", (session['user_id'],))
    user_details = cur.fetchone()
    cur.close()

    return render_template('dashboard.html', name=session['name'], user_details=user_details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
