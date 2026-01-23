from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        sems = list(map(float, request.form.get("sems").split(",")))

        # SIMPLE prediction (average method – safe)
        predicted = sum(sems) / len(sems)

        return render_template(
            "result.html",
            title="Predicted Next CGPA",
            result=round(predicted, 2)
        )

    return render_template("predict.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)



     

