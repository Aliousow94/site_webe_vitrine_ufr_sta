from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.utils import secure_filename
import os
import pymysql

app = Flask(__name__)
app.secret_key = "ufrsta"

app.config['UPLOAD_FOLDER_ACTUALITES'] = 'static/uploads/actualites'
app.config['UPLOAD_FOLDER_ACTIVITES'] = 'static/uploads/activites'
app.config['UPLOAD_FOLDER_GALERIE'] = 'static/uploads/galerie'

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="ufr_sta",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def index():
    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    
    curseur.execute("SELECT * FROM actualite ORDER BY date_publication DESC LIMIT 3")
    dernieres_actualites = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("index.html", dernieres_actualites=dernieres_actualites)


@app.route("/formation")
def formation():
    connexion = get_db_connection()
    curseur = connexion.cursor()

    # Récupérer les départements
    curseur.execute("SELECT * FROM departement ORDER BY nom ASC")
    departements = curseur.fetchall()

    # Récupérer les formations avec le nom de leur département
    curseur.execute("""
        SELECT f.*, d.nom as nom_departement 
        FROM formation f 
        LEFT JOIN departement d ON f.departement_id = d.id
        ORDER BY d.nom ASC, f.niveau ASC
    """)
    formations = curseur.fetchall()

    # Regrouper les formations par département
    formations_par_dept = {}
    for f in formations:
        dept_id = f.get('departement_id')
        if dept_id:
            if dept_id not in formations_par_dept:
                formations_par_dept[dept_id] = {
                    'nom_departement': f['nom_departement'],
                    'formations': []
                }
            formations_par_dept[dept_id]['formations'].append(f)
        else:
            if 'sans_dept' not in formations_par_dept:
                formations_par_dept['sans_dept'] = {'nom_departement': 'Autres formations', 'formations': []}
            formations_par_dept['sans_dept']['formations'].append(f)

    curseur.close()
    connexion.close()
    
    return render_template("formation.html", formations_par_dept=formations_par_dept)
@app.route("/departement")
def departement():
    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    # Récupérer tous les départements
    curseur.execute("SELECT * FROM departement ORDER BY nom ASC")
    departements = curseur.fetchall()
    
    # BONUS : Récupérer les formations pour les lier à leurs départements
    curseur.execute("""
        SELECT f.*, d.nom as nom_departement 
        FROM formation f 
        LEFT JOIN departement d ON f.departement_id = d.id
    """)
    toutes_formations = curseur.fetchall()
   
    formations_par_dept = {}
    for f in toutes_formations:
        if f['departement_id']:
            dept_id = f['departement_id']
            if dept_id not in formations_par_dept:
                formations_par_dept[dept_id] = []
            formations_par_dept[dept_id].append(f)

    curseur.close()
    connexion.close()
    
    return render_template("departement.html", departements=departements, formations_par_dept=formations_par_dept)

@app.route("/actualites")
def actualites():
    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM actualite ORDER BY date_publication DESC")
    actualites = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("actualites.html", actualites=actualites)

@app.route("/activites")
def activites():

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    
    curseur.execute("SELECT * FROM activite ORDER BY date_activite,id DESC")
    activites = curseur.fetchall()
    
    
    for act in activites:
        curseur.execute("SELECT photo FROM photo_activite WHERE id_activite=%s", (act['id'],))
        act['photos'] = curseur.fetchall()
        
    curseur.close()
    connexion.close()
    return render_template("activites.html",activites=activites)
@app.route("/enseignant")
def enseignant():
    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    
    sql = """
        SELECT e.*, d.nom as nom_departement 
        FROM enseignant e 
        LEFT JOIN departement d ON e.departement_id = d.id
        ORDER BY e.nom ASC
    """
    curseur.execute(sql)
    enseignants = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("enseignant.html", enseignants=enseignants)
@app.route("/gallery")
def gallery():
    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    # Récupérer tous les albums
    curseur.execute("SELECT * FROM galerie ORDER BY date_album DESC")
    albums = curseur.fetchall()
    
    # Pour chaque album, chercher sa première photo et le nombre total de photos
    for alb in albums:
        curseur.execute("SELECT photo FROM photo_galerie WHERE galerie_id=%s ORDER BY id ASC LIMIT 1", (alb['id'],))
        premiere_photo = curseur.fetchone()
        
        curseur.execute("SELECT COUNT(*) as total FROM photo_galerie WHERE galerie_id=%s", (alb['id'],))
        total_photos = curseur.fetchone()
        
        alb['photos'] = [] 
        if premiere_photo:
            alb['photos'].append(premiere_photo)
        alb['total_photos'] = total_photos['total']

    curseur.close()
    connexion.close()
    
    return render_template("gallery.html", albums=albums)
@app.route("/contact")

def contact():
    if request.method == "POST":
        nom = request.form["nom"]
        email = request.form["email"]
        sujet = request.form["sujet"]
        message = request.form["message"]

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO contact (nom, email, sujet, message) VALUES (%s, %s, %s, %s)"
        curseur.execute(sql, (nom, email, sujet, message))
        connexion.commit()
        curseur.close()
        connexion.close()
        
        return redirect(url_for("contact"))
    return render_template("contact.html")



@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        motdepasse = request.form["motdepasse"]

        connexion = get_db_connection()
        curseur = connexion.cursor()
        
        sql = "SELECT * FROM administrateur WHERE email=%s AND motdepasse=%s"
        curseur.execute(sql, (email, motdepasse))
        admin = curseur.fetchone()
        
        curseur.close()
        connexion.close()

        if admin:
            session["admin"] = admin["nom"]
            return redirect(url_for("dashboard"))

        return "Email ou mot de passe incorrect"

    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    # --- Compteurs ---
    curseur.execute("SELECT COUNT(*) as nb FROM actualite")
    nb_actualites = curseur.fetchone()

    curseur.execute("SELECT COUNT(*) as nb FROM activite")
    nb_activites = curseur.fetchone()

    curseur.execute("SELECT COUNT(*) as nb FROM formation")
    nb_formations = curseur.fetchone()

    curseur.execute("SELECT COUNT(*) as nb FROM galerie")
    nb_albums = curseur.fetchone()

    curseur.execute("SELECT COUNT(*) as nb FROM enseignant")
    nb_enseignants = curseur.fetchone()

    curseur.execute("SELECT COUNT(*) as nb FROM contact")
    nb_messages = curseur.fetchone()

    curseur.close()
    connexion.close()
    
    return render_template("admin/dashboard.html", 
                           nb_actualites=nb_actualites, 
                           nb_activites=nb_activites, 
                           nb_formations=nb_formations, 
                           nb_albums=nb_albums, 
                           nb_enseignants=nb_enseignants, 
                           nb_messages=nb_messages)

@app.route("/admin/actualite")
def liste_actualite():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM actualite ORDER BY date_publication DESC")
    actualites = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_actualite.html", actualites=actualites)

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
        photo.save(os.path.join(app.config["UPLOAD_FOLDER_ACTUALITES"], nom_photo))

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO actualite (titre, date_publication, description, photo) VALUES (%s, %s, %s, %s)"
        curseur.execute(sql, (titre, date_publication, description, nom_photo))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_actualite"))

    return render_template("admin/ajouter_actualite.html")

@app.route("/admin/actualite/modifier/<int:id>", methods=["GET", "POST"])
def modifier_actualite(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        titre = request.form["titre"]
        date_publication = request.form["date_publication"]
        description = request.form["description"]
        
        nom_photo = request.form.get("ancienne_photo")
        photo = request.files["photo"]
        
        if photo.filename != "":
            nom_photo = secure_filename(photo.filename)
            photo.save(os.path.join(app.config["UPLOAD_FOLDER_ACTUALITES"], nom_photo))

        sql = "UPDATE actualite SET titre=%s, date_publication=%s, description=%s, photo=%s WHERE id=%s"
        curseur.execute(sql, (titre, date_publication, description, nom_photo, id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_actualite"))

    curseur.execute("SELECT * FROM actualite WHERE id=%s", (id,))
    actualite = curseur.fetchone()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/modifier_actualite.html", actualite=actualite)

@app.route("/admin/actualite/supprimer/<int:id>", methods=["POST"])
def supprimer_actualite(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT photo FROM actualite WHERE id=%s", (id,))
    actualite = curseur.fetchone()
    
    if actualite and actualite['photo']:
        chemin = os.path.join(app.config["UPLOAD_FOLDER_ACTUALITES"], actualite['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)

    curseur.execute("DELETE FROM actualite WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_actualite"))

@app.route("/admin/activite")
def liste_activite():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM activite ORDER BY date_activite DESC")
    activites = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_activite.html", activites=activites)

@app.route("/admin/activite/ajouter", methods=["GET", "POST"])
def ajouter_activite():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        titre = request.form["titre"]
        date_activite = request.form["date_activite"]
        lieu = request.form["lieu"]
        organisateur = request.form["organisateur"]
        description = request.form["description"]

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO activite (titre, date_activite, lieu, organisateur, description) VALUES (%s, %s, %s, %s, %s)"
        curseur.execute(sql, (titre, date_activite, lieu, organisateur, description))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_activite"))

    return render_template("admin/ajouter_activite.html")

@app.route("/admin/activite/modifier/<int:id>", methods=["GET", "POST"])
def modifier_activite(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        titre = request.form["titre"]
        date_activite = request.form["date_activite"]
        lieu = request.form["lieu"]
        organisateur = request.form["organisateur"]
        description = request.form["description"]

        sql = "UPDATE activite SET titre=%s, date_activite=%s, lieu=%s, organisateur=%s, description=%s WHERE id=%s"
        curseur.execute(sql, (titre, date_activite, lieu, organisateur, description, id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_activite"))

    curseur.execute("SELECT * FROM activite WHERE id=%s", (id,))
    activite = curseur.fetchone()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/modifier_activite.html", activite=activite)

@app.route("/admin/activite/supprimer/<int:id>", methods=["POST"])
def supprimer_activite(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT photo FROM photo_activite WHERE id_activite=%s", (id,))
    photos = curseur.fetchall()
    for p in photos:
        chemin = os.path.join(app.config["UPLOAD_FOLDER_ACTIVITES"], p['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)

    curseur.execute("DELETE FROM activite WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_activite"))

@app.route("/admin/activite/<int:activite_id>/photos")
def gestion_photos_activite(activite_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM activite WHERE id=%s", (activite_id,))
    activite = curseur.fetchone()
    
    curseur.execute("SELECT * FROM photo_activite WHERE id_activite=%s", (activite_id,))
    photos = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/photo_activite.html", activite=activite, photos=photos)

@app.route("/admin/activite/<int:activite_id>/photos/ajouter", methods=["POST"])
def ajouter_photo_activite(activite_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        fichiers = request.files.getlist("photos")
        
        connexion = get_db_connection()
        curseur = connexion.cursor()
        
        for fichier in fichiers:
            if fichier and fichier.filename != "":
                nom_fichier = secure_filename(fichier.filename)
                nom_final = f"act{activite_id}_{nom_fichier}"
                fichier.save(os.path.join(app.config["UPLOAD_FOLDER_ACTIVITES"], nom_final))
                
                sql = "INSERT INTO photo_activite (id_activite, photo) VALUES (%s, %s)"
                curseur.execute(sql, (activite_id, nom_final))
                
        connexion.commit()
        curseur.close()
        connexion.close()

    return redirect(url_for("gestion_photos_activite", activite_id=activite_id))

@app.route("/admin/photo/supprimer/<int:photo_id>", methods=["POST"])
def supprimer_photo_activite(photo_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM photo_activite WHERE id=%s", (photo_id,))
    photo = curseur.fetchone()

    if photo:
        activite_id = photo['id_activite']
        chemin = os.path.join(app.config["UPLOAD_FOLDER_ACTIVITES"], photo['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)
            
        curseur.execute("DELETE FROM photo_activite WHERE id=%s", (photo_id,))
        connexion.commit()
        
        curseur.close()
        connexion.close()
        
        return redirect(url_for("gestion_photos_activite", activite_id=activite_id))

    curseur.close()
    connexion.close()
    return redirect(url_for("liste_activite"))

# GESTION DE LA GALERIE 

app.config['UPLOAD_FOLDER_GALERIE'] = 'static/uploads/galerie'


@app.route("/admin/galerie")
def liste_galerie():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM galerie ORDER BY date_album DESC")
    albums = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_galerie.html", albums=albums)


@app.route("/admin/galerie/ajouter", methods=["GET", "POST"])
def ajouter_galerie():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        titre = request.form["titre"]
        description = request.form["description"]
        date_album = request.form["date_album"]

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO galerie (titre, description, date_album) VALUES (%s, %s, %s)"
        curseur.execute(sql, (titre, description, date_album))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_galerie"))

    return render_template("admin/ajouter_galerie.html")
# Route publique pour récupérer les photos d'un album (pour le Modal en JS)
@app.route("/admin/galerie/<int:galerie_id>/photos/json")
def photos_galerie_json(galerie_id):
    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM photo_galerie WHERE galerie_id=%s", (galerie_id,))
    photos = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    # Conversion pour le format JSON
    result = [{'id': p['id'], 'photo': p['photo']} for p in photos]
    return jsonify(result)


@app.route("/admin/galerie/supprimer/<int:id>", methods=["POST"])
def supprimer_galerie(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    
    curseur.execute("SELECT photo FROM photo_galerie WHERE galerie_id=%s", (id,))
    photos = curseur.fetchall()
    for p in photos:
        chemin = os.path.join(app.config["UPLOAD_FOLDER_GALERIE"], p['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)

    
    curseur.execute("DELETE FROM galerie WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_galerie"))


@app.route("/admin/galerie/<int:galerie_id>/photos")
def photos_galerie(galerie_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM galerie WHERE id=%s", (galerie_id,))
    album = curseur.fetchone()
    
    curseur.execute("SELECT * FROM photo_galerie WHERE galerie_id=%s", (galerie_id,))
    photos = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/photos_galerie.html", album=album, photos=photos)


@app.route("/admin/galerie/<int:galerie_id>/photos/ajouter", methods=["POST"])
def ajouter_photo_galerie(galerie_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        fichiers = request.files.getlist("photos")
        
        connexion = get_db_connection()
        curseur = connexion.cursor()
        
        for fichier in fichiers:
            if fichier and fichier.filename != "":
                nom_fichier = secure_filename(fichier.filename)
                nom_final = f"gal{galerie_id}_{nom_fichier}"
                fichier.save(os.path.join(app.config["UPLOAD_FOLDER_GALERIE"], nom_final))
                
                sql = "INSERT INTO photo_galerie (galerie_id, photo) VALUES (%s, %s)"
                curseur.execute(sql, (galerie_id, nom_final))
                
        connexion.commit()
        curseur.close()
        connexion.close()

    return redirect(url_for("photos_galerie", galerie_id=galerie_id))


@app.route("/admin/galerie/photo/supprimer/<int:photo_id>", methods=["POST"])
def supprimer_photo_galerie(photo_id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT * FROM photo_galerie WHERE id=%s", (photo_id,))
    photo = curseur.fetchone()

    if photo:
        galerie_id = photo['galerie_id']
        chemin = os.path.join(app.config["UPLOAD_FOLDER_GALERIE"], photo['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)
            
        curseur.execute("DELETE FROM photo_galerie WHERE id=%s", (photo_id,))
        connexion.commit()
        
        curseur.close()
        connexion.close()
        
        return redirect(url_for("photos_galerie", galerie_id=galerie_id))

    curseur.close()
    connexion.close()
    return redirect(url_for("liste_galerie"))

# GESTION DES FORMATIONS 


# 1. Lister les formations
@app.route("/admin/formation")
def liste_formation():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    # On fait une jointure pour récupérer le nom du département au lieu de juste l'ID
    sql = """
        SELECT f.*, d.nom as nom_departement 
        FROM formation f 
        LEFT JOIN departement d ON f.departement_id = d.id
    """
    curseur.execute(sql)
    formations = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_formation.html", formations=formations)

# 2. Ajouter une formation
@app.route("/admin/formation/ajouter", methods=["GET", "POST"])
def ajouter_formation():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        nom = request.form["nom"]
        niveau = request.form["niveau"]
        duree = request.form["duree"]
        admission = request.form["admission"]
        debouches = request.form["debouches"]
        departement_id = request.form.get("departement_id") or None

        # ASSEMBLAGE DU PROGRAMME : On récupère les 6 semestres et on les structure
        programme_final = ""
        for i in range(1, 7):
            champ = request.form.get(f"sem{i}", "").strip()
            if champ:
                programme_final += f"Semestre {i} :\n{champ}\n\n"
        
        programme_final = programme_final.strip() # Enlève le saut de ligne à la fin

        sql = """
        INSERT INTO formation (nom, niveau, duree, admission, debouches, programme, departement_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        curseur.execute(sql, (nom, niveau, duree, admission, debouches, programme_final, departement_id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_formation"))

    curseur.execute("SELECT * FROM departement")
    departements = curseur.fetchall()
    
    curseur.close()
    connexion.close()

    return render_template("admin/ajouter_formation.html", departements=departements)
# 3. Modifier une formation
@app.route("/admin/formation/modifier/<int:id>", methods=["GET", "POST"])
def modifier_formation(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        nom = request.form["nom"]
        niveau = request.form["niveau"]
        duree = request.form["duree"]
        admission = request.form["admission"]
        debouches = request.form["debouches"]
        programme = request.form["programme"]
        departement_id = request.form.get("departement_id") or None

        sql = """
        UPDATE formation 
        SET nom=%s, niveau=%s, duree=%s, admission=%s, debouches=%s, programme=%s, departement_id=%s 
        WHERE id=%s
        """
        curseur.execute(sql, (nom, niveau, duree, admission, debouches, programme, departement_id, id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_formation"))

    
    curseur.execute("SELECT * FROM formation WHERE id=%s", (id,))
    formation = curseur.fetchone()
    
    curseur.execute("SELECT * FROM departement")
    departements = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/modifier_formation.html", formation=formation, departements=departements)

# 4. Supprimer une formation
@app.route("/admin/formation/supprimer/<int:id>", methods=["POST"])
def supprimer_formation(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM formation WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_formation"))
@app.route("/admin/contact")
def liste_contact():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM contact ORDER BY date_envoi DESC")
    contacts = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_contact.html", contacts=contacts)
@app.route("/admin/contact/supprimer/<int:id>", methods=["POST"])
def supprimer_contact(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM contact WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_contact"))


@app.route("/admin/departement")
def liste_departement():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM departement ORDER BY nom ASC")
    departements = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_departement.html", departements=departements)

@app.route("/admin/departement/ajouter", methods=["GET", "POST"])
def ajouter_departement():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nom = request.form["nom"]
        description = request.form["description"]
        responsable = request.form["responsable"]
        contact = request.form["contact"]

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO departement (nom, description, responsable, contact) VALUES (%s, %s, %s, %s)"
        curseur.execute(sql, (nom, description, responsable, contact))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_departement"))

    return render_template("admin/ajouter_departement.html")

@app.route("/admin/departement/modifier/<int:id>", methods=["GET", "POST"])
def modifier_departement(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        nom = request.form["nom"]
        description = request.form["description"]
        responsable = request.form["responsable"]
        contact = request.form["contact"]

        sql = "UPDATE departement SET nom=%s, description=%s, responsable=%s, contact=%s WHERE id=%s"
        curseur.execute(sql, (nom, description, responsable, contact, id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_departement"))

    curseur.execute("SELECT * FROM departement WHERE id=%s", (id,))
    departement = curseur.fetchone()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/modifier_departement.html", departement=departement)

@app.route("/admin/departement/supprimer/<int:id>", methods=["POST"])
def supprimer_departement(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("DELETE FROM departement WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_departement"))

# --- GESTION DES ENSEIGNANTS (ADMIN) ---

@app.route("/admin/enseignant")
def liste_enseignant():
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    # Jointure pour récupérer le nom du département au lieu de juste l'ID
    sql = """
        SELECT e.*, d.nom as nom_departement 
        FROM enseignant e 
        LEFT JOIN departement d ON e.departement_id = d.id
        ORDER BY e.nom ASC
    """
    curseur.execute(sql)
    enseignants = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/liste_enseignant.html", enseignants=enseignants)

@app.route("/admin/enseignant/ajouter", methods=["GET", "POST"])
def ajouter_enseignant():
    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        nom = request.form["nom"]
        grade = request.form["grade"]
        departement_id = request.form.get("departement_id") or None
        email = request.form["email"]
        domaine_recherche = request.form["domaine_recherche"]
        
        photo = request.files["photo"]
        nom_photo = ""
        if photo and photo.filename != "":
            nom_photo = secure_filename(photo.filename)
            photo.save(os.path.join('static/uploads/enseignants', nom_photo))

        connexion = get_db_connection()
        curseur = connexion.cursor()
        sql = "INSERT INTO enseignant (nom, grade, departement_id, email, domaine_recherche, photo) VALUES (%s, %s, %s, %s, %s, %s)"
        curseur.execute(sql, (nom, grade, departement_id, email, domaine_recherche, nom_photo))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_enseignant"))

    # Récupérer la liste des départements pour le menu déroulant
    connexion = get_db_connection()
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM departement ORDER BY nom ASC")
    departements = curseur.fetchall()
    curseur.close()
    connexion.close()

    return render_template("admin/ajouter_enseignant.html", departements=departements)

@app.route("/admin/enseignant/modifier/<int:id>", methods=["GET", "POST"])
def modifier_enseignant(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()

    if request.method == "POST":
        nom = request.form["nom"]
        grade = request.form["grade"]
        departement_id = request.form.get("departement_id") or None
        email = request.form["email"]
        domaine_recherche = request.form["domaine_recherche"]
        
        nom_photo = request.form.get("ancienne_photo")
        photo = request.files["photo"]
        
        if photo and photo.filename != "":
            nom_photo = secure_filename(photo.filename)
            photo.save(os.path.join('static/uploads/enseignants', nom_photo))

        sql = "UPDATE enseignant SET nom=%s, grade=%s, departement_id=%s, email=%s, domaine_recherche=%s, photo=%s WHERE id=%s"
        curseur.execute(sql, (nom, grade, departement_id, email, domaine_recherche, nom_photo, id))
        connexion.commit()
        
        curseur.close()
        connexion.close()

        return redirect(url_for("liste_enseignant"))

    curseur.execute("SELECT * FROM enseignant WHERE id=%s", (id,))
    enseignant = curseur.fetchone()
    
    curseur.execute("SELECT * FROM departement ORDER BY nom ASC")
    departements = curseur.fetchall()
    
    curseur.close()
    connexion.close()
    
    return render_template("admin/modifier_enseignant.html", enseignant=enseignant, departements=departements)

@app.route("/admin/enseignant/supprimer/<int:id>", methods=["POST"])
def supprimer_enseignant(id):
    if "admin" not in session:
        return redirect(url_for("login"))

    connexion = get_db_connection()
    curseur = connexion.cursor()
    
    curseur.execute("SELECT photo FROM enseignant WHERE id=%s", (id,))
    enseignant = curseur.fetchone()
    
    if enseignant and enseignant['photo']:
        chemin = os.path.join('static/uploads/enseignants', enseignant['photo'])
        if os.path.exists(chemin):
            os.remove(chemin)

    curseur.execute("DELETE FROM enseignant WHERE id=%s", (id,))
    connexion.commit()
    
    curseur.close()
    connexion.close()

    return redirect(url_for("liste_enseignant"))
@app.route("/admin/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)