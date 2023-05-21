from flask import Flask, jsonify, request
from faker import Faker
import csv
import requests

app = Flask(__name__)

fake = Faker()


@app.route('/')
def options():
    return '<p>Access http://127.0.0.1:5000/requirements to print out the content of requirements.txt file<br>Access ' \
           'http://127.0.0.1:5000/generate-users/?count=20 to generate any number of random users<br>Access ' \
           'http://127.0.0.1:5000/mean to return average height and weight from hw.csv file<br>Access ' \
           'http://127.0.0.1:5000/astros to return number of astros from API at the moment</p>'


# 1 return the content of requirements file
@app.route('/requirements')
def get_requirements_content():
    with open('requirements.txt', 'r') as file:
        content = file.read()
        formatted_content = content.replace('\n', '<br>')
    return formatted_content


# 2 return specific number of randomly generated users (name+email)
@app.route('/generate-users/')
def generate_users():
    count = request.args.get('count', default=1, type=int)
    users = []
    for _ in range(count):
        name = fake.name()
        email = fake.email()
        user = name + ' ' + email
        users.append(user)
    return users


heights = []
weights = []


# return the average height (cm)  and weight (kg) from the file attached
@app.route('/mean/')
def calculate_mean():
    heights = []
    weights = []
    with open('hw.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            height = float((row[1]).strip()) * 2.54
            weight = float((row[2]).strip()) * 0.45359237
            heights.append(height)
            weights.append(weight)

    m_height = sum(heights) / len(heights)
    m_weight = sum(weights) / len(weights)

    return jsonify({
        'mean_height, cm': m_height,
        'mean_weight, kg': m_weight
    })


# 4 return number of astros at the moment from API
@app.route('/astros')
def get_astros():
    url = 'http://api.open-notify.org/astros.json'

    response = requests.get(url)
    data = response.json()

    astros = data['number']
    return jsonify({'Number of astros at the moment': astros})


if __name__ == '__main__':
    app.run()
