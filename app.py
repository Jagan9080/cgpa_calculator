from flask import Flask, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# VIT grade mapping
GRADE_POINTS = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "E": 5,
    "F": 0
}

@app.route("/")
def home():
    return render_template("index.html")

# 1️⃣ VIT SEMESTER CGPA
@app.route("/sem_avg", methods=["GET", "POST"])
def sem_avg():
    if request.method == "POST":
        credits = list(map(int, request.form.get("credits").split(",")))
        grades = request.form.get("grades").split(",")

        points = [GRADE_POINTS[g.strip().upper()] for g in grades]
        cgpa = sum(c*p for c,p in zip(credits, points)) / sum(credits)

        return render_template("result.html",
                               title="VIT Semester CGPA",
                               result=round(cgpa, 2))
    return render_template("sem_avg.html")

# 2️⃣ YEAR-WISE CGPA
@app.route("/year", methods=["GET", "POST"])
def year():
    if request.method == "POST":
        year_cgpas = list(map(float, request.form.get("years").split(",")))
        return render_template("result.html",
                               title="VIT Year-wise CGPA",
                               result=round(np.mean(year_cgpas), 2))
    return render_template("year_cgpa.html")

# 3️⃣ CREDIT BASED CGPA (PURE VIT)
@app.route("/credit", methods=["GET", "POST"])
def credit():
    if request.method == "POST":
        credits = list(map(int, request.form.get("credits").split(",")))
        grades = request.form.get("grades").split(",")

        points = [GRADE_POINTS[g.strip().upper()] for g in grades]
        cgpa = sum(c*p for c,p in zip(credits, points)) / sum(credits)

        return render_template("result.html",
                               title="VIT Credits CGPA",
                               result=round(cgpa, 2))
    return render_template("credit_cgpa.html")

# 4️⃣ MIXED CGPA
@app.route("/mixed", methods=["GET", "POST"])
def mixed():
    if request.method == "POST":
        year_cgpa = list(map(float, request.form.get("years").split(",")))
        sem_cgpa = list(map(float, request.form.get("sems").split(",")))

        total = ((sum(year_cgpa) * 2) + sum(sem_cgpa)) / ((len(year_cgpa) * 2) + len(sem_cgpa))

        return render_template("result.html",
                               title="VIT Mixed CGPA",
                               result=round(total, 2))
    return render_template("mixed_cgpa.html")

# 5️⃣ PREDICT NEXT CGPA (ML)
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        sems = list(map(float, request.form.get("sems").split(",")))

        X = np.array([[sems[i]] for i in range(len(sems)-1)])
        y = np.array(sems[1:])

        model = LinearRegression()
        model.fit(X, y)

        predicted = model.predict([[sems[-1]]])[0]

        return render_template("result.html",
                               title="Predicted Next CGPA",
                               result=round(predicted, 2))
    return render_template("predict.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    app.run(host="0.0.0.0", port=port)



     
