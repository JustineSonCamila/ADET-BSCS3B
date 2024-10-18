# app.py
from flask import Flask, render_template, request

app = Flask(__name__)

# Route to display form for user input
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission and display the result
@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name')  # Get the name entered in the form
    return render_template('greet.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
