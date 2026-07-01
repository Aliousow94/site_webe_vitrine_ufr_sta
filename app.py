from flask import Flask , render_template,redirect,url_for,request,session
from werkzeug.utils import secure_filename
import os
import pymysql

app=Flask(__name__)
app.secret_key = "ufrsta"

app.config["UPLOAD_FOLDER"] = "static/images"

connexion=pymysql.connect(host="localhost",user="root",password="",database="ufr_sta"
)



@app.route("/")
def index():
    return render_template("index.html")
@app.route("/formation")
def formation():
    
    return render_template("formation.html")
@app.route("/departement")
def departement():
    return render_template("departement.html")
@app.route("/actualites")
def actualites():
    return render_template("actualites.html")
@app.route("/activites")
def activites():
    return render_template("activites.html")
@app.route("/enseignant")
def enseignant():
    return render_template("enseignant.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")
@app.route("/admin/actualite")
def liste_actualite():

    curseur = connexion.cursor()

    curseur.execute("""
        SELECT *
        FROM actualite
    """)

    actualite = curseur.fetchall()

    return render_template(
        "admin/liste_actualite.html",
        actualite=actualite
    )
@app.route("/admin/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("admin/dashboard.html")
    

@app.route("/admin/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        curseur = connexion.cursor()

        sql = """
        SELECT *
        FROM administrateur
        WHERE email=%s
        AND motdepasse=%s
        """

        curseur.execute(sql, (email, motdepasse))

        admin = curseur.fetchone()

        if admin:

            session["admin"] = admin[1]

            return redirect(url_for("dashboard"))

        return "Email ou mot de passe incorrect"

    return render_template("admin/login.html")




@app.route("/admin/actualite/ajouter", methods=["GET", "POST"])
def ajouter_actualite():
    if "admin" not in session:
        return redirect(url_for("login"))


    if request.method == "POST":

        titre = request.form["titre"]
        date_publication = request.form["date_publication"]
        description = request.form["description"]

        photo = request.files["photo"]

        nom_photo = secure_filename(photo.filename)

        photo.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                nom_photo
            )
        )

        curseur = connexion.cursor()

        sql = """
        INSERT INTO actualite
        (titre, date_publication, description, photo)
        VALUES (%s, %s, %s, %s)
        """

        curseur.execute(
            sql,
            (
                titre,
                date_publication,
                description,
                nom_photo
            )
        )

        connexion.commit()

        return redirect(url_for("liste_actualite"))

    return render_template("admin/ajouter_actualite.html")




if __name__ == "__main__":
    
    app.run(debug=True)