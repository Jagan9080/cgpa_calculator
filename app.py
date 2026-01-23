from flask import Flask, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- SIMPLE ROUTES ----------------
@app.route("/sem_avg", methods=["GET", "POST"])
def sem_avg():
    return render_template("sem_avg.html")


@app.route("/year", methods=["GET", "POST"])
def year():
    return render_template("year.html")


@app.route("/credit", methods=["GET", "POST"])
def credit():
    return render_template("credit.html")


@app.route("/mixed", methods=["GET", "POST"])
def mixed():
    return render_template("mixed.html")


# ---------------- CGPA PREDICTION (ML) ----------------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        sems = list(map(float, request.form.get("sems").split(",")))

        X = np.array([[sems[i]] for i in range(len(sems)-1)])
        y = np.array(sems[1:])

        model = LinearRegression()
        model.fit(X, y)

        predicted = model.predict([[sems[-1]]])[0]

        return render_template(
            "result.html",
            title="Predicted Next CGPA",
            result=round(predicted, 2)
        )

    return render_template("predict.html")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



     


