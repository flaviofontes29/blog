from flask import Flask, render_template
import requests

app = Flask(__name__)

post = requests.get("https://api.npoint.io/8aaed9cdfdcd7eece7df").json()


@app.route("/")
def home():
    return render_template("index.html", all_posts=post)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/post<int:index>")
def show_post(index):
    requested_post = None
    for blog_posts in post:
        if blog_posts['id'] == index:
            requested_post = blog_posts
    return render_template("post.html", posts=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
