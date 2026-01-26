from flask import Flask, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# VIT / College grade points
GRADE_POINTS = {
    "S": 10,
    "A": 9,
    "B": 8,
    "C": 7,
    "D": 6,
    "E": 5,
    "F": 0
}

# ---------- Helpers ----------
def parse_list(text):
    """Parse comma separated values like: '8.1, 8.2, 9' """
    if not text:
        return []
    parts = [p.strip() for p in text.replace("\n", ",").split(",")]
    parts = [p for p in parts if p != ""]
    return parts

def parse_float_list(text):
    return [float(x) for x in parse_list(text)]

def parse_int_list(text):
    return [int(float(x)) for x in parse_list(text)]

def parse_grade_list(text):
    grades = [g.strip().upper() for g in parse_list(text)]
    for g in grades:
        if g not in GRADE_POINTS:
            raise ValueError(f"Invalid grade: {g}")
    return grades

def calculate_cgpa_from_credits(credits, grades):
    """credits list + grades list -> CGPA"""
    if len(credits) != len(grades):
        raise ValueError("Credits count and Grades count must be same")

    total_credits = sum(credits)
    if total_credits == 0:
        raise ValueError("Total credits cannot be 0")

    total_points = 0
    for c, g in zip(credits, grades):
        total_points += c * GRADE_POINTS[g]

    return round(total_points / total_credits, 2)


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("index.html")


# ✅ 1) Semester CGPA (Credits + Grades)  (Correct)
@app.route("/sem_avg", methods=["GET", "POST"])
def sem_avg():
    if request.method == "POST":
        try:
            credits = parse_int_list(request.form.get("credits"))
            grades = parse_grade_list(request.form.get("grades"))

            cgpa = calculate_cgpa_from_credits(credits, grades)
            return render_template("result.html",
                                   title="Semester CGPA (Credits Based)",
                                   result=cgpa)
        except Exception as e:
            return render_template("result.html",
                                   title="Error",
                                   result=str(e))

    return render_template("sem_avg.html")


# ✅ 2) Year wise CGPA (Average of year CGPAs)
@app.route("/year", methods=["GET", "POST"])
def year():
    if request.method == "POST":
        try:
            years = parse_float_list(request.form.get("years"))
            if len(years) == 0:
                raise ValueError("Enter at least 1 year CGPA")
            result = round(float(np.mean(years)), 2)

            return render_template("result.html",
                                   title="Year-wise CGPA",
                                   result=result)
        except Exception as e:
            return render_template("result.html",
                                   title="Error",
                                   result=str(e))

    return render_template("year_cgpa.html")


# ✅ 3) Credits CGPA (Credits + Grades) (Correct)
@app.route("/credit", methods=["GET", "POST"])
def credit():
    if request.method == "POST":
        try:
            credits = parse_int_list(request.form.get("credits"))
            grades = parse_grade_list(request.form.get("grades"))

            cgpa = calculate_cgpa_from_credits(credits, grades)
            return render_template("result.html",
                                   title="Credits CGPA (College Style)",
                                   result=cgpa)
        except Exception as e:
            return render_template("result.html",
                                   title="Error",
                                   result=str(e))

    return render_template("credit_cgpa.html")


# ✅ 4) Mixed CGPA (Weighted using credits)
# User enters:
# Semester CGPAs: 8.1, 8.3, 8.6
# Semester Credits: 20, 22, 21
@app.route("/mixed", methods=["GET", "POST"])
def mixed():
    if request.method == "POST":
        try:
            cgpas = parse_float_list(request.form.get("cgpas"))
            credits = parse_int_list(request.form.get("credits"))

            if len(cgpas) != len(credits):
                raise ValueError("Number of CGPAs and Credits must be same")

            total_credits = sum(credits)
            if total_credits == 0:
                raise ValueError("Total credits cannot be 0")

            total = 0
            for c, g in zip(credits, cgpas):
                total += c * g

            mixed_cgpa = round(total / total_credits, 2)

            return render_template("result.html",
                                   title="Mixed CGPA (Weighted)",
                                   result=mixed_cgpa)
        except Exception as e:
            return render_template("result.html",
                                   title="Error",
                                   result=str(e))

    return render_template("mixed_cgpa.html")


# ✅ 5) Predict Next CGPA (Robust input)
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        try:
            sems = parse_float_list(request.form.get("sems"))

            if len(sems) < 2:
                raise ValueError("Enter at least 2 previous semester CGPAs")

            X = np.array([[sems[i]] for i in range(len(sems) - 1)])
            y = np.array(sems[1:])

            model = LinearRegression()
            model.fit(X, y)

            next_cgpa = round(float(model.predict([[sems[-1]]])[0]), 2)

            return render_template("result.html",
                                   title="Predicted Next Semester CGPA",
                                   result=next_cgpa)
        except Exception as e:
            return render_template("result.html",
                                   title="Error",
                                   result=str(e))

    return render_template("predict.html")


# ✅ For deployment everywhere
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
