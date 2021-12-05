
import requests
from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message

app = Flask(__name__)

post = requests.get("https://api.npoint.io/8aaed9cdfdcd7eece7df").json()

# Config Send Email
app.secret_key = "SpfLFpf"
mail_settings = {
    "MAIL_SERVER": "smtp.gmail.com",
    "MAIL_PORT": 465,
    "MAIL_USE_TSL": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "seu_email",
    "MAIL_PASSWORD": "sua_senha",
}
app.config.update(mail_settings)
mail = Mail(app)


@app.route("/")
def home():
    return render_template("index.html", all_posts=post)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        msg= Message(
            subject=f"{data['name']} te enviou uma mensagem no Portfólio",
            sender=app.config.get("MAIL_USERNAME"),
            recipients=[
                "contato.flaviofontes@gmail.com",
                app.config.get("MAIL_USERNAME"),
            ],
            body=f"""
                        {data['name']} com o e-mail {data['email']} e telefone {data['phone']}
                        te enviou a sequinte menssagem:

                        {data['message']}
                    """,
        )
        try:
            mail.send(msg)
            flash("Mensagem enviada com sucesso!", "success")

        except Exception:
            flash("Erro ao enviar a sua mensagem!", "danger")

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
