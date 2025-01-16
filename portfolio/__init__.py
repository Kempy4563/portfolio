from flask import request
from flask import Flask, render_template, abort, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)
app.secret_key = os.environ.get('RENDER_SECRET_KEY', default='your secret key')


projects = [
    {
        "name": "Air Fryer Recipe App",
        "thumb": "img/airfryer.png",
        "hero": "img/airfryer.png",
        "categories": ["python", "django"],
        "slug": "Air-Fryer-Recipe-App",
        "prod": "https://airfryer-recipes.onrender.com/",
    },
    {
        "name": "Atomic Habits",
        "thumb": "img/atomic_habits.png",
        "hero": "img/atomic_habits.png",
        "categories": ["python", "web"],
        "slug": "atomic-habits",
        "prod": "https://habit-tracker-dbb6.onrender.com/",
    },
    {
        "name": "Mini Blog",
        "thumb": "img/miniblog.png",
        "hero": "img/miniblog.png",
        "categories": ["python", "web"],
        "slug": "micro-blog",
        "prod": "https://python-microblog-sxxb.onrender.com/",
    },
    {
        "name": "Weather App",
        "thumb": "img/open_weather.png",
        "hero": "img/weather_hero.png",
        "categories": ["python", "API", "web"],
        "slug": "open-weather",
        "prod": "https://kempy-weather.streamlit.app/",
    },
]

slug_to_project = {project["slug"]: project for project in projects}


@app.route("/")
def home():
    return render_template("home.html", projects=projects)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Two ways to do this:
# - either store everything about a project in Python and populate a generic `project.html` template.
# - or as done here, have separate templates for each project
# At the end of the day, we have to write the project info somewhere, and HTML is a great tool for that.
# This allows each project to be slightly different as we choose,
# And with Jinja2 we can always reuse parts of the code as macros (more on that, later!)
@app.route("/project/<string:slug>")
def project(slug):
    if slug not in slug_to_project:
        abort(404)
    return render_template(f"project_{slug}.html", project=slug_to_project[slug])


def send_email(to, subject, message):
    from_email = "leekempson73@gmail.com"  # replace with your email
    password = os.environ.get('RENDER_EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to, text)
    server.quit()

@app.route('/contact', methods=['GET', 'POST'])
def handle_contact_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        subject = "Contact Form Submission"
        message_body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        send_email("leekempson@hotmail.com", subject, message_body)

        flash('Thank you for your inquiry!', 'success')
        flash('I will get back to you asap.', 'success')

    return render_template('contact.html')
