from flask import Flask, render_template, request

app = Flask(__name__)

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
def index():
    return render_template('index.html')

@app.route('/credit', methods=['GET', 'POST'])
def credit():
    cgpa = None
    if request.method == 'POST':
        try:
            credits = list(map(int, request.form['credits'].split(',')))
            grades = request.form['grades'].split(',')

            total = sum(c * GRADE_POINTS[g.strip().upper()]
                        for c, g in zip(credits, grades))
            cgpa = round(total / sum(credits), 2)
        except:
            cgpa = "Invalid Input"

    return render_template('credit.html', cgpa=cgpa)

@app.route('/sem_avg', methods=['GET', 'POST'])
def sem_avg():
    avg = None
    if request.method == 'POST':
        try:
            values = list(map(float, request.form['sems'].split(',')))
            avg = round(sum(values) / len(values), 2)
        except:
            avg = "Invalid Input"
    return render_template('sem_avg.html', avg=avg)

@app.route('/year', methods=['GET', 'POST'])
def year():
    avg = None
    if request.method == 'POST':
        try:
            years = list(map(float, request.form['years'].split(',')))
            avg = round(sum(years) / len(years), 2)
        except:
            avg = "Invalid Input"
    return render_template('year.html', avg=avg)

@app.route('/mixed', methods=['GET', 'POST'])
def mixed():
    avg = None
    if request.method == 'POST':
        try:
            years = int(request.form['years'])
            sems = int(request.form['sems'])
            avg = round((years + sems) / 2, 2)
        except:
            avg = "Invalid Input"
    return render_template('mixed.html', avg=avg)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None
    if request.method == 'POST':
        try:
            sems = int(request.form['sems'])
            result = f"Expected CGPA after {sems} semesters"
        except:
            result = "Invalid Input"
    return render_template('predict.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
