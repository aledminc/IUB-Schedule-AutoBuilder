from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("Homepage.html")

@app.route("/build-schedule", methods=["POST"])
def build_schedule():
    aar_pdf = request.files["aar_pdf"]
    semester = request.form["semester"]
    num_classes = int(request.form["num_classes"])
    difficulty = int(request.form["difficulty"])
    must_have = request.form["must_have"]

    # Save PDF locally if needed
    aar_pdf.save("user_aar.pdf")

    return redirect(url_for("schedule"))


@app.route("/schedule")
def schedule():
    # Here you can pass any data you need to show in the schedule page
    return render_template("Schedule.html")

if __name__ == "__main__":
    app.run(debug=True)