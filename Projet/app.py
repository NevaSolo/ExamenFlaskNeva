from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.urandom(24)

# Configurations de la base de données
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'frame'
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect_page', methods=['GET', 'POST'])
def redirect_page():
    button_clicked = request.form['button_clicked']

    if button_clicked == 'inscription':
        return redirect(url_for('register'))
    elif button_clicked == 'connexion':
        return redirect(url_for('login'))

        # Aucun bouton n'a été cliqué, restez sur index.html
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        username = session['user']
        welcome_message = f'Bienvenue, {username}!'
        return render_template('login.html', welcome_message=welcome_message)
    else:
        if request.method == 'POST':
            try:
                # Récupérer les valeurs du formulaire
                email = request.form['email']
                password = request.form['password']

                # Connexion à la base de données MySQL
                conn = mysql.connector.connect(**db_config)

                # Création d'un curseur
                cursor = conn.cursor()

                # Exécution de la requête de sélection pour les voitures
                select_voitures_query = "SELECT id, nom, image_url, model, matriculation, couleur, prix FROM voiture"
                cursor.execute(select_voitures_query)
                voitures = cursor.fetchall()

                # Affichage des données dans la console
                # Exécution de la requête de vérification de l'utilisateur basée sur l'email et le mot de passe
                select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
                cursor.execute(select_query, (email, password))

                

                # Récupération du résultat de la requête
                user = cursor.fetchone()

                # Fermeture de la connexion
                conn.close()

                # Affichage des données récupérées dans la console

                if user:
                    session['user'] = user[1]  # Stocker le nom d'utilisateur dans la session
                    flash('Connexion réussie', 'success')
                    return render_template('accueil.html', voitures=voitures)
                else:
                    flash('Échec de la connexion. Vérifiez votre email et votre mot de passe.', 'danger')
                    

            except mysql.connector.Error as e:
                # Affichage d'une erreur si la connexion à la base de données échoue
                print("Erreur de connexion à la base de données MySQL:", e)
                flash('Erreur lors de la soumission du formulaire.', 'danger')

    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Récupérer les valeurs du formulaire d'inscription
            user_name = request.form['user']
            email = request.form['email']
            password = request.form['password']

            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(**db_config)

            # Création d'un curseur
            cursor = conn.cursor()

            # Exécution de la requête de sélection pour les voitures
            select_voitures_query = "SELECT id, nom, image_url, model, matriculation, couleur, prix FROM voiture"
            cursor.execute(select_voitures_query)
            voitures = cursor.fetchall()

            # Exécution de la requête d'insertion pour l'inscription
            insert_query = "INSERT INTO users (user, email, password) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (user_name, email, password))

            # Validation des changements dans la base de données
            conn.commit()

            # Fermeture de la connexion
            conn.close()

            flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
            return render_template('accueil.html',voitures=voitures)

        except mysql.connector.Error as e:
            # Affichage d'une erreur si la connexion à la base de données échoue
            print("Erreur de connexion à la base de données MySQL:", e)
            flash('Erreur lors de l\'inscription.', 'danger')

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('login'))

@app.route('/accueil')
def accueil():
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(**db_config)
         # Création d'un curseur
        cursor = conn.cursor()

       # Exécution de la requête de sélection pour les voitures
        select_voitures_query = "SELECT id, nom, image_url, model, matriculation, couleur, prix FROM voiture"
        cursor.execute(select_voitures_query)
        voitures = cursor.fetchall()

        # Fermeture de la connexion
        conn.close()

        return render_template('accueil.html', voitures=voitures)

    except mysql.connector.Error as e:
        print("Erreur lors de la récupération des voitures:", e)

@app.route('/reserve/<string:nom>')
def reserve(nom):
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Exécuter la requête pour récupérer les détails de la voiture sélectionnée
        select_query = "SELECT nom, image_url, model, matriculation, couleur, prix FROM voiture WHERE nom = %s"
        cursor.execute(select_query, (nom,))
        voitures = cursor.fetchone()

        # Fermeture de la connexion à la base de données
        conn.close()

        if voitures:
            return render_template('reservation.html', voitures=voitures)
        else:
            flash('Voiture non trouvée', 'danger')
            return redirect(url_for('reserve'))

    except mysql.connector.Error as e:
        print("Erreur lors de la récupération des détails de la voiture:", e)
        flash('Erreur lors de la récupération des détails de la voiture. Veuillez réessayer.', 'danger')
        return redirect(url_for('reserve'))

@app.route('/res')
def res():
    return render_template('reservation.html')


# Route pour la page de réservation
@app.route('/reservation', methods=['POST'])
def reservation():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        model = request.form['model']
        prix = request.form['prix']
        date = request.form['date']
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Exécuter la requête d'insertion
            insert_query = "INSERT INTO reserver (nom, model, prix, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (nom, model, prix, date))

            # Valider la transaction
            conn.commit()

            # Fermer le curseur et la connexion à la base de données
            cursor.close()
            conn.close()

            # Rediriger l'utilisateur vers une page de confirmation
            flash('Votre réservation a été enregistrée avec succès!', 'success')
            return redirect(url_for('confirmation'))
    
        except mysql.connector.Error as e:
            # En cas d'erreur lors de l'insertion, annuler la transaction et afficher un message d'erreur
            print("Erreur lors de l'insertion des données dans la table reserve:", e)
            flash('Erreur lors de l\'enregistrement de votre réservation. Veuillez réessayer.', 'danger')
            return redirect(url_for('reservation'))
    return 'Méthode non autorisée', 405
# Route pour la page de confirmation
@app.route('/confirmation')
def confirmation():
    # Afficher une page de confirmation après avoir enregistré les données
    return render_template('confirmation.html')

@app.route('/loc')
def loc():
    # Afficher une page de confirmation après avoir enregistré les données
    return render_template('location.html')

# Route pour la page de réservation
@app.route('/location', methods=['POST'])
def location():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        adresse = request.form['adresse']
        model = request.form['model']
        prix = request.form['prix']
        date = request.form['date']
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Exécuter la requête d'insertion
            insert_query = "INSERT INTO location (nom, adresse, model, prix, date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (nom, adresse, model, prix, date))

            # Valider la transaction
            conn.commit()

            # Fermer le curseur et la connexion à la base de données
            cursor.close()
            conn.close()

            # Rediriger l'utilisateur vers une page de confirmation
            flash('Votre réservation a été enregistrée avec succès!', 'success')
            return redirect(url_for('confirm'))
    
        except mysql.connector.Error as e:
            # En cas d'erreur lors de l'insertion, annuler la transaction et afficher un message d'erreur
            print("Erreur lors de l'insertion des données dans la table reserve:", e)
            flash('Erreur lors de l\'enregistrement de votre réservation. Veuillez réessayer.', 'danger')
            return redirect(url_for('location'))
    return 'Méthode non autorisée', 405
# Route pour la page de confirmation
@app.route('/confirm')
def confirm():
    # Afficher une page de confirmation après avoir enregistré les données
    return render_template('confirm.html')

@app.route('/liste_location')
def liste_location():
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(**db_config)
         # Création d'un curseur
        cursor = conn.cursor()

        # Exécution de la requête de sélection
        select_query = "SELECT * FROM location"
        cursor.execute(select_query)

        # Récupération des résultats
        location = cursor.fetchall()

        # Fermeture de la connexion
        conn.close()

        return render_template('list_location.html', location=location)

    except mysql.connector.Error as e:
        print("Erreur lors de la récupération des voitures:", e)

@app.route('/liste_reservation')
def liste_reservation():
    try:
        # Connexion à la base de données MySQL
        conn = mysql.connector.connect(**db_config)
         # Création d'un curseur
        cursor = conn.cursor()

        # Exécution de la requête de sélection
        select_query = "SELECT * FROM reserver"
        cursor.execute(select_query)

        # Récupération des résultats
        reserver = cursor.fetchall()

        # Fermeture de la connexion
        conn.close()

        return render_template('list_reservation.html', reserver=reserver)

    except mysql.connector.Error as e:
        print("Erreur lors de la récupération des voitures:", e)

@app.route('/delete_location/<int:id>', methods=['POST'])
def delete_location(id):
    if request.method == 'POST':
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Exécution de la requête de suppression
            delete_query = "DELETE FROM location WHERE id = %s"
            cursor.execute(delete_query, (id,))

            # Valider la transaction
            conn.commit()

            # Fermer le curseur et la connexion à la base de données
            cursor.close()
            conn.close()

            flash('La location a été supprimée avec succès!', 'success')
            return redirect(url_for('liste_location'))

        except mysql.connector.Error as e:
            print("Erreur lors de la suppression de la location:", e)
            flash('Erreur lors de la suppression de la location. Veuillez réessayer.', 'danger')
            return redirect(url_for('liste_location'))

    return 'Méthode non autorisée', 405

@app.route('/delete_reservation/<int:id>', methods=['POST'])
def delete_reservation(id):
    if request.method == 'POST':
        try:
            # Connexion à la base de données MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Exécution de la requête de suppression
            delete_query = "DELETE FROM reserver WHERE id = %s"
            cursor.execute(delete_query, (id,))

            # Valider la transaction
            conn.commit()

            # Fermer le curseur et la connexion à la base de données
            cursor.close()
            conn.close()

            flash('La réservation a été supprimée avec succès!', 'success')
            return redirect(url_for('liste_reservation'))

        except mysql.connector.Error as e:
            print("Erreur lors de la suppression de la réservation:", e)
            flash('Erreur lors de la suppression de la réservation. Veuillez réessayer.', 'danger')
            return redirect(url_for('liste_reservation'))

    return 'Méthode non autorisée', 405


if __name__ == '__main__':
    app.run(debug=True)
