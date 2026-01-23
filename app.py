from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Grade to points (VIT style)
GRADE_POINTS = {
    'S': 10,
    'A': 9,
    'B': 8,
    'C': 7,
    'D': 6,
    'E': 5,
    'F': 0
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/credit', methods=['GET', 'POST'])
def credit():
    cgpa = None
    if request.method == 'POST':
        credits = list(map(int, request.form['credits'].split(',')))
        grades = request.form['grades'].split(',')

        total_points = 0
        total_credits = sum(credits)

        for c, g in zip(credits, grades):
            total_points += c * GRADE_POINTS[g.strip().upper()]

        cgpa = round(total_points / total_credits, 2)

    return render_template('credit.html', cgpa=cgpa)

@app.route('/year', methods=['GET', 'POST'])
def year():
    cgpa = None
    if request.method == 'POST':
        values = list(map(float, request.form['cgpas'].split(',')))
        cgpa = round(sum(values) / len(values), 2)

    return render_template('year.html', cgpa=cgpa)

@app.route('/sem_avg', methods=['GET', 'POST'])
def sem_avg():
    cgpa = None
    if request.method == 'POST':
        values = list(map(float, request.form['cgpas'].split(',')))
        cgpa = round(sum(values) / len(values), 2)

    return render_template('sem_avg.html', cgpa=cgpa)

@app.route('/mixed', methods=['GET', 'POST'])
def mixed():
    cgpa = None
    if request.method == 'POST':
        credits = list(map(int, request.form['credits'].split(',')))
        grades = request.form['grades'].split(',')

        total_points = 0
        total_credits = sum(credits)

        for c, g in zip(credits, grades):
            total_points += c * GRADE_POINTS[g.strip().upper()]

        cgpa = round(total_points / total_credits, 2)

    return render_template('mixed.html', cgpa=cgpa)

@app.route('/predict')
def predict():
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
