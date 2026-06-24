from flask import Flask , render_template,redirect,url_for,request
import mysql.connector
app=Flask(__name__)
connexion=mysql.connector.connect(host="localhost",user="root",password="",database="ufr_sta")
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/formation")
def formation():
    curseur= connexion.cursor()
    curseur.execute("select * from formation ")
    formations=curseur.fetchall()
    return render_template("formation.html",formations=formations)
@app.route("/departement")
def departement():
    return render_template("departement.html")
@app.route("/actualites")
def actualites():
    return render_template("actualites.html")
@app.route("/activites")
def activites():
    return render_template("activites.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/gallery")
def gallery():
    return render_template("gallery.html")
@app.route("/ajouter",methods=["GET","POST"])
def ajouter():
    if request.method=="POST" :
       nom=request.form["nom"]
       niveau=request.form["niveau"]
       curseur=connexion.cursor()
       sql="insert into formation(nom,niveau)values(%s,%s)"
       valeur=(nom,niveau)
       curseur.execute(sql,valeur)
       connexion.commit()
       return redirect(url_for("formation"))
    return render_template("ajouter.html")
@app.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):

    curseur = connexion.cursor()

    if request.method == "POST":

        nom = request.form["nom"]
        niveau = request.form["niveau"]

        sql = """
        UPDATE formation
        SET nom=%s, niveau=%s
        WHERE id=%s
        """

        curseur.execute(sql, (nom, niveau, id))
        connexion.commit()

        return redirect(url_for("formation"))

    curseur.execute("SELECT * FROM formation WHERE id=%s", (id,))
    formation = curseur.fetchone()

    return render_template("modifier.html", formation=formation)



if __name__ == "__main__":
    app.run(debug=True)
    