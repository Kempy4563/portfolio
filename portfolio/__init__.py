from flask import Flask, render_template, abort

app = Flask(__name__)
projects = [
    {
        "name": "Mini Blog",
        "thumb": "img/miniblog.png",
        "hero": "img/miniblog.png",
        "categories": ["python", "web"],
        "slug": "micro-blog",
        "prod": "https://python-microblog-sxxb.onrender.com/",
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
        "name": "Air Fryer Recipe App",
        "thumb": "img/airfryer.png",
        "hero": "img/airfryer.png",
        "categories": ["python", "django"],
        "slug": "Air-Fryer-Recipe-App",
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




@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404