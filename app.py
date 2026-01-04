from flask import Flask, render_template, request
import csv


app = Flask(__name__)
try:
    with open("screening_results.csv", "x", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "name",
            "age",
            "temperature",
            "days_unwell",
            "cough",
            "breathing_difficulty",
            "chest_pain",
            "total_score",
            "risk_level"
        ])
except FileExistsError:
    pass


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    name = request.form["name"]
    age = int(request.form["age"])
    temperature = float(request.form["temperature"])
    days_unwell = int(request.form["days_unwell"])
    cough = request.form["cough"]
    breathing_difficulty = request.form["breathing_difficulty"]
    chest_pain = request.form["chest_pain"]


    # Risk scoring 
    score = 0
    if age >= 60:
        score += 2
    if temperature >= 38.0:
        score += 2
    if temperature >= 39.0:
        score += 3
    if cough == "yes":
        score += 1
    if days_unwell >= 3:
        score += 1
    if breathing_difficulty == "yes":
        score += 3
    if chest_pain == "yes":
        score += 3

    if score >= 6:
        risk_level = "High Risk,See a doctor immediately"
    elif 3 <= score < 6:
        risk_level = "Moderate Risk, Monitor your symptoms closely"
    else:
        risk_level = "Low Risk, Maintain good hygiene and rest"

    #save to csv
    with open("screening_results.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            name,
            age,
            temperature,
            days_unwell,
            cough,
            breathing_difficulty,
            chest_pain,
            score,
            risk_level
        ])
    

    return render_template(
        "result.html",
        name=name,
        score=score,
        risk_level=risk_level
    )

if __name__ == "__main__":
    app.run()

