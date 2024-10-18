from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'camila_key' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'adet'

mysql = MySQL(app)

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
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute(""" 
            INSERT INTO users (name, middle_name, last_name, age, email, contact, address, password) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, middle_name, last_name, age, email, contact, address, hashed_password))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, hashed_password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user'] = {
                'id': user[0],
                'name': user[1],
                'middle_name': user[2],
                'last_name': user[3],
                'age': user[4],
                'email': user[5],
                'contact': user[6],
                'address': user[7],
            }
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('app.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', user_details=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
