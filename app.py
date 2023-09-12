import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import login_required, apology

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["IMAGE_UPLOADS"] = "/workspaces/91915796/pset10/project/uploads"

Session(app)


db = SQL("sqlite:///portfolio.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Username or password wrong honey!", 401)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/admin")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(password)

        # Ensure password was submitted correctly
        if password != confirmation:
            flash('Passwords must be igual')
            return render_template("register.html")


    # Query database for username
        rows = db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, password_hash)

        flash('New User Registered')
        return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():

    row = db.execute("SELECT username FROM users WHERE id= ?", session["user_id"])
    user = row[0]["username"]
    date = datetime.now()
    projects = []
    blogposts = []


    if request.method == "POST":

        # Create the variables to insert in database projects
        ptitle = request.form.get("project-title")
        ptools = request.form.get("project-tools")
        pimage = request.files.get("project-image")
        pdesc = request.form.get("project-description")
        pcont = request.form.get("project-content")

        if ptitle:
            # If the title was sent Create Project in database
            rows = db.execute("INSERT INTO projects(title, tools, description, content, datetime) VALUES(?, ?, ?, ?, ?)", ptitle, ptools, pdesc, pcont, date)

            idp = db.execute("SELECT id FROM projects WHERE title = ? ORDER BY datetime DESC", ptitle)
            if pimage:
                pimage.filename = "project" + str(idp[0]["id"]) + ".jpg"
                pimage.save(os.path.join(app.config["IMAGE_UPLOADS"], pimage.filename))
                rows = db.execute("UPDATE projects SET image = ? WHERE id = ?", pimage.filename, idp[0]["id"])


        # Create the variables to insert in database blog
        btitle = request.form.get("post-title")
        bkeys = request.form.get("post-keys")
        bimage = request.files.get("post-image")
        bdesc = request.form.get("post-description")
        bcont = request.form.get("post-content")

        if btitle:
            # If the title was sent Create Blog post in database
            rows = db.execute("INSERT INTO blog(title, keywords, description, content, datetime) VALUES(?, ?, ?, ?, ?)", btitle, bkeys, bdesc, bcont, date)

            idb = db.execute("SELECT id FROM blog WHERE title = ? ORDER BY datetime DESC", btitle)
            if bimage:
                bimage.filename = "blog" + str(idb[0]["id"]) + ".jpg"
                bimage.save(os.path.join(app.config["IMAGE_UPLOADS"], bimage.filename))
                rows = db.execute("UPDATE blog SET image = ? WHERE id = ?", bimage.filename, idb[0]["id"])



        # Making Searchs on Projects and Blogs

        sproject = request.form.get("search-project")

        # If There is a Search for a Project:
        if sproject:
            search = "%" + sproject + "%"
            searchp = db.execute("SELECT id, title, tools, datetime FROM projects WHERE title LIKE ?", search)
            projects = searchp

        spost = request.form.get("search-post")

         # If There is a Search for a Blog post:
        if spost:
            search = "%" + spost + "%"
            searchp = db.execute("SELECT id, title, keywords, datetime FROM blog WHERE title LIKE ?", search)
            blogposts = searchp


    return render_template("admin.html", username=user, projects=projects, blogposts=blogposts)


@app.route("/delete-post/<id>")
@login_required
def delete_post(id):

    row = db.execute("DELETE FROM blog WHERE id = ?", id)

    return redirect("/admin")


@app.route("/edit-post/<id>", methods=["GET", "POST"])
@login_required
def edit_post(id):

    post = db.execute("SELECT id, title, keywords, description, content FROM blog WHERE id = ?", id)
    post = post[0]

    if request.method == "POST":
        btitle = request.form.get("post-title")
        bkeys = request.form.get("post-keys")
        bimage = request.files.get("post-image")
        bdesc = request.form.get("post-description")
        bcont = request.form.get("post-content")

        rows = db.execute("UPDATE blog SET title = ?, keywords = ?, description = ?, content = ? WHERE id = ?", btitle, bkeys, bdesc, bcont, id)

        if bimage:
            bimage.filename = "blog" + str(id) + ".jpg"
            bimage.save(os.path.join(app.config["IMAGE_UPLOADS"], bimage.filename))
            rows = db.execute("UPDATE blog SET image = ? WHERE id = ?", bimage.filename, id)

        return redirect("/admin")



    return render_template("edit-post.html", post=post)


@app.route("/delete-project/<id>")
@login_required
def delete_project(id):

    row = db.execute("DELETE FROM projects WHERE id = ?", id)

    return redirect("/admin")



@app.route("/edit-project/<id>", methods=["GET", "POST"])
@login_required
def edit_project(id):

    project = db.execute("SELECT id, title, tools, description, content FROM projects WHERE id = ?", id)
    project = project[0]

    if request.method == "POST":
        ptitle = request.form.get("project-title")
        ptools = request.form.get("project-tools")
        pimage = request.files.get("project-image")
        pdesc = request.form.get("project-description")
        pcont = request.form.get("project-content")

        rows = db.execute("UPDATE projects SET title = ?, tools = ?, description = ?, content = ? WHERE id = ?", ptitle, ptools, pdesc, pcont, id)

        if pimage:
            pimage.filename = "project" + str(id) + ".jpg"
            pimage.save(os.path.join(app.config["IMAGE_UPLOADS"], pimage.filename))

            rows = db.execute("UPDATE project SET image = ? WHERE id = ?", pimage.filename, id)

        return redirect("/admin")


    return render_template("edit-project.html", project=project)




@app.route("/")
def index():

    return render_template("index.html")

@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/projects")
def projects():

    projects = db.execute("SELECT id, title, image, description FROM projects")


    return render_template("projects.html", projects=projects)

@app.route("/project-content/<id>")
def project_content(id):

    project = db.execute("SELECT * FROM projects WHERE id = ?", id)
    project = project[0]

    return render_template("project-content.html", project=project)


@app.route("/blog")
def blog():

    posts = db.execute("SELECT id, title, image, description FROM blog")


    return render_template("blog.html", posts=posts)


@app.route("/blog-content/<id>")
def blog_content(id):

    post = db.execute("SELECT * FROM blog WHERE id = ?", id)
    post = post[0]

    return render_template("blog-content.html", post=post)



@app.route("/uploads/<name>")
def download_file(name):

    return send_from_directory(app.config["IMAGE_UPLOADS"], name)



