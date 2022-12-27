from flask import Flask, request, render_template, redirect, flash, session, g
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",                 # à modifier
            user="mnourry3",                     # à modifier
            password="2909",                # à modifier
            database="BDD_mnourry3",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('layout.html')


### TABLEAU ###
@app.route('/tableaux/show')
def show_tableau():
    bdd = get_db().cursor()
    sql = """SELECT *
             FROM tableau
             LEFT JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque
             ORDER BY id_tableau"""
    bdd.execute(sql)
    tableau = bdd.fetchall()
    return render_template('tableaux/show_tableaux.html', tableau=tableau)


@app.route('/tableaux/add', methods=['GET'])
def add_tableau():
    bdd = get_db().cursor()
    sql = """SELECT *
             FROM type_epoque
             ORDER BY id_type_epoque"""
    bdd.execute(sql)
    type_epoque = bdd.fetchall()
    return render_template('tableaux/add_tableau.html', type_epoque=type_epoque)


@app.route('/tableaux/add', methods=['POST'])
def valid_add_tableau():
    nom = request.form.get('nom', '')
    prixAssurance = request.form.get('prix-assurance', '')
    dateRealisation = request.form.get('date-realisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('musee', '')
    mouvement = request.form.get('mouvement', '')
    photo = request.form.get('photo', '')
    typeEpoque_id = request.form.get('epoque', '')

    bdd = get_db().cursor()
    sql = """INSERT INTO tableau(
              nom_tableau,
              prix_assurance,
              date_realisation,
              peintre,
              localisation_musee,
              mouvement,
              photo,
              type_epoque_id)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    bdd.execute(sql, [nom, prixAssurance, dateRealisation, peintre, localisationMusee, mouvement, photo, typeEpoque_id])
    get_db().commit()

    message = u'Tableau ajouté, Nom: '+ nom + ', Prix assurance: ' + prixAssurance + '€, Date réalisation: ' + dateRealisation + ', Peintre: '+ peintre + ', Musée: ' + localisationMusee + ', Mouvement: ' + mouvement + ', Photo: ' + photo + ', Epoque ID: ' + typeEpoque_id
    flash(message, 'alert-success')
    return redirect('/tableaux/show')


@app.route('/tableaux/delete', methods=['GET'])
def delete_tableau():
    id_tableau = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM tableau WHERE id_tableau = %s"
    bdd.execute(sql, [id_tableau])
    get_db().commit()
    message = u'Un tableau supprimé, ID: ' + id_tableau
    flash(message, 'alert-danger')
    return redirect('/tableaux/show')


@app.route('/tableaux/edit', methods=['GET'])
def edit_tableau():
    id_tableau = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT tableau.*, type_epoque.*
             FROM tableau
             LEFT JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque
             WHERE id_tableau = %s"""
    bdd.execute(sql, [id_tableau])
    tableaux = bdd.fetchone()

    bdd2 = get_db().cursor()
    sql2 = """SELECT type_epoque.*
              FROM type_epoque"""
    bdd2.execute(sql2)
    type_epoque = bdd2.fetchall()
    return render_template('tableaux/edit_tableau.html', tableau=tableaux, type_epoque=type_epoque)


@app.route('/tableaux/edit', methods=['POST'])
def valid_edit_tableau():
    id_tableau = request.form.get('id', '')
    nom = request.form.get('nom', '')
    prixAssurance = request.form.get('prix-assurance', '')
    dateRealisation = request.form.get('date-realisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('musee', '')
    mouvement = request.form.get('mouvement', '')
    typeEpoque_id = request.form.get('epoque', '')
    photo = request.form.get('photo', '')

    bdd = get_db().cursor()
    sql = """UPDATE tableau
             SET nom_tableau = %s,
                 prix_assurance = %s,
                 date_realisation = %s,
                 peintre = %s,
                 localisation_musee = %s,
                 mouvement = %s,
                 type_epoque_id = %s,
                 photo = %s
                 WHERE id_tableau = %s"""
    bdd.execute(sql, [nom, prixAssurance, dateRealisation, peintre, localisationMusee, mouvement, typeEpoque_id, photo, id_tableau])
    get_db().commit()

    message = u'Tableau modifié, Nom: ' + nom + ", Prix de l'assurance: " + prixAssurance + '€, Date de réalisation: ' + dateRealisation + ', Peintre: ' + peintre + ', Musée: ' + localisationMusee + ', Mouvement: ' + mouvement + ', ID Epoque: ' + typeEpoque_id
    flash(message, 'alert-warning')
    return redirect('/tableaux/show')


### CARDS ###
@app.route('/cards/show')
def show_cards():
    bdd = get_db().cursor()
    sql = """SELECT *
              FROM tableau
              ORDER BY id_tableau"""

    bdd.execute(sql)
    tableau = bdd.fetchall()
    return render_template('cards/show_cards.html', tableaux=tableau)


@app.route('/cards/edit', methods=['GET'])
def edit_cards():
    id_tableau = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = """SELECT tableau.*, type_epoque.*
             FROM tableau
             LEFT JOIN type_epoque ON tableau.type_epoque_id = type_epoque.id_type_epoque
             WHERE id_tableau = %s"""
    bdd.execute(sql, [id_tableau])
    tableaux = bdd.fetchone()

    bdd2 = get_db().cursor()
    sql2 = """SELECT type_epoque.*
              FROM type_epoque"""
    bdd2.execute(sql2)
    type_epoque = bdd2.fetchall()
    return render_template('cards/edit_cards.html', tableau=tableaux, type_epoque=type_epoque)


@app.route('/cards/edit', methods=['POST'])
def valid_edit_cards():
    id_tableau = request.form.get('id', '')
    nom = request.form.get('nom', '')
    prixAssurance = request.form.get('prix-assurance', '')
    dateRealisation = request.form.get('date-realisation', '')
    peintre = request.form.get('peintre', '')
    localisationMusee = request.form.get('musee', '')
    mouvement = request.form.get('mouvement', '')
    typeEpoque_id = request.form.get('epoque', '')
    photo = request.form.get('photo', '')

    bdd = get_db().cursor()
    sql = """UPDATE tableau
             SET nom_tableau = %s,
                 prix_assurance = %s,
                 date_realisation = %s,
                 peintre = %s,
                 localisation_musee = %s,
                 mouvement = %s,
                 type_epoque_id = %s,
                 photo = %s
                 WHERE id_tableau = %s"""
    bdd.execute(sql, [nom, prixAssurance, dateRealisation, peintre, localisationMusee, mouvement, typeEpoque_id, photo, id_tableau])
    get_db().commit()

    message = u'Tableau modifié, Nom: ' + nom + ", Prix de l'assurance: " + prixAssurance + '€, Date de réalisation: ' + dateRealisation + ', Peintre: ' + peintre + ', Musée: ' + localisationMusee + ', Mouvement: ' + mouvement + ', ID Epoque: ' + typeEpoque_id
    flash(message, 'alert-warning')
    return redirect('/cards/show')


@app.route('/cards/delete', methods=['GET'])
def delete_cards():
    id_tableau = request.args.get('id', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM tableau WHERE id_tableau = %s"
    bdd.execute(sql, [id_tableau])
    get_db().commit()
    message = u'Un tableau supprimé, ID: ' + id_tableau
    flash(message, 'alert-danger')
    return redirect('/cards/show')


### TYPE EPOQUE ###
@app.route('/type_epoque/show')
def show_type_epoque():
    bdd = get_db().cursor()
    sql = """SELECT *
             FROM type_epoque
             ORDER BY id_type_epoque"""
    bdd.execute(sql)
    type_epoque = bdd.fetchall()
    return render_template('type_epoque/show_type_epoque.html', type_epoque=type_epoque)


@app.route('/type_epoque/add', methods=['GET'])
def add_type_epoque():
    return render_template('type_epoque/add_type_epoque.html')


@app.route('/type_epoque/add', methods=['POST'])
def valid_add_type_epoque():
    libelle = request.form.get('libelle', '')
    bdd = get_db().cursor()
    sql = """INSERT INTO type_epoque(libelle)
             VALUES (%s)"""
    bdd.execute(sql, [libelle])
    get_db().commit()
    message = u'Type ajouté, Libellé: ' + libelle
    flash(message, 'alert-success')
    return redirect('/type_epoque/show')


@app.route('/type_epoque/delete', methods=['GET'])
def delete_type_article():
    id_type_epoque = request.args.get('idepoque', '')
    bdd = get_db().cursor()
    sql = "DELETE FROM type_epoque WHERE id_type_epoque = %s"
    bdd.execute(sql, [id_type_epoque])
    get_db().commit()
    message = u'Type d\'époque supprimé, ID: ' + id_type_epoque
    flash(message, 'alert-danger')
    return redirect('/type_epoque/show')


@app.route('/type_epoque/edit', methods=['GET'])
def edit_type_article():
    id = request.args.get('id', '')
    return render_template('type_epoque/edit_type_epoque.html', type_epoque=type_epoque)


@app.route('/type_epoque/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id = request.form.get('id', '')
    message=u"Type d'époque modifié, ID: " + id + ", Libellé: " + libelle
    flash(message, 'alert-warning')
    return redirect('/type_epoque/show')


if __name__ == '__main__':
    app.run()
