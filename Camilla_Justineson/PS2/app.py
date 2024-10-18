from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Function to read from JSON file
def read_json():
    with open('form_data.json', 'r') as file:
        data = json.load(file)
    return data

# Function to write to JSON file
def write_json(data):
    with open('form_data.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = read_json()
        
        # Update data with form inputs
        data['name'] = request.form.get('name')
        data['middle_name'] = request.form.get('midname')
        data['last_name'] = request.form.get('last_name')
        data['age'] = request.form.get('age')
        data['email'] = request.form.get('email')
        data['contact'] = request.form.get('contact')
        data['address'] = request.form.get('address')
        
        # Write the updated data back to the JSON file
        write_json(data)
        
        return render_template('app.html', data=data)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
