from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.j2")

@app.get("/404")
def error404():
    return render_template("404.j2")

@app.get("/about")
def about():
    return render_template("about.j2")

@app.get("/appointment")
def appointment():
    return render_template("appointment.j2")

@app.get("/contacts")
def contacts():
    return render_template("contacts.j2")

@app.get("/course-page")
def course():
    return render_template("course-page.j2")

@app.get("/courses")
def courses():
    return render_template("courses.j2")

@app.get("/faq")
def faq():
    return render_template("faq.j2")

@app.get("/feature")
def feature():
    return render_template("feature.j2")

@app.get("/legal-info")
def info():
    return render_template("legal-info.j2")

@app.get("/payment")
def payment():
    return render_template("payment.j2")

@app.get("/team")
def team():
    return render_template("team.j2")

@app.get("/testimonial")
def testimonial():
    return render_template("testimonial.j2")

if __name__ == "__main__":
    app.run(host="0", port=5000)
