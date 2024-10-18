from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
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

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO users (name, middle_name, last_name, age, email, contact, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (name, middle_name, last_name, age, email, contact, address))
        mysql.connection.commit()
        cur.close()

        data = {
            'name': name,
            'middle_name': middle_name,
            'last_name': last_name,
            'age': age,
            'email': email,
            'contact': contact,
            'address': address
        }

        return render_template('app.html', data=data)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
