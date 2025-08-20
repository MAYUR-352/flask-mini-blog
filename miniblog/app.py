from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from miniblog.models import db, Post, Comment

app = Flask(__name__)


# Ensure instance folder exists
INSTANCE_FOLDER = os.path.join(os.path.dirname(__file__), "instance")
db_path = os.path.join(INSTANCE_FOLDER, "database.db")
if not os.path.exists(INSTANCE_FOLDER):
    os.makedirs(INSTANCE_FOLDER)

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
#     "SQLALCHEMY_DATABASE_URI", f"sqlite:///{db_path}"
#     )
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///local.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")


# File upload config
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db.init_app(app)


# Helper function for allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Create tables automatically
@app.before_request
def create_tables():
    db.create_all()


# Homepage with search
@app.route("/", methods=["GET"])
def index():
    search_query = request.args.get("q", "")
    if search_query:
        posts = (
            Post.query.filter(
                (Post.title.contains(search_query))
                | (Post.content.contains(search_query))
            )
            .order_by(Post.created_at.desc())
            .all()
        )
    else:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template(
        "index.html",
        posts=posts,
        search_query=search_query,
        current_year=datetime.now().year,
    )


# Add post
@app.route("/add", methods=["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        author = request.form.get("author", "Anonymous")
        tags = request.form.get("tags", "")

        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = (
                    f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))
                image_filename = unique_filename

        post = Post(
            title=title,
            content=content,
            author=author,
            tags=tags,
            image_filename=image_filename,
        )
        db.session.add(post)
        db.session.commit()
        flash("Post added successfully!", "success")
        return redirect(url_for("index"))
    return render_template("add_post.html", current_year=datetime.now().year)


# Edit post
@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        post.author = request.form.get("author", post.author)
        post.tags = request.form.get("tags", post.tags)

        if "image" in request.files:
            file = request.files["image"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = (
                    f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                )
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_filename))
                post.image_filename = unique_filename

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for("view_post", post_id=post.id))
    return render_template(
        "edit_post.html", post=post, current_year=datetime.now().year
    )


# Delete post
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted.", "info")
    return redirect(url_for("index"))


# View post + comments
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        author = request.form.get("author", "Anonymous")
        content = request.form["content"]
        comment = Comment(post_id=post.id, author=author, content=content)
        db.session.add(comment)
        db.session.commit()
        flash("Comment added!", "success")
        return redirect(url_for("view_post", post_id=post.id))

    comments = (
        Comment.query.filter_by(post_id=post.id)
        .order_by(Comment.created_at.desc())
        .all()
    )
    return render_template(
        "view_post.html", post=post, comments=comments, current_year=datetime.now().year
    )


if __name__ == "__main__":
    app.run(debug=True)
