DROP TABLE IF EXISTS tableau;
DROP TABLE IF EXISTS type_epoque;

CREATE TABLE type_epoque(
  id_type_epoque INT(5) NOT NULL AUTO_INCREMENT,
  libelle VARCHAR(255),
  PRIMARY KEY (id_type_epoque)
);

CREATE TABLE tableau(
    id_tableau INT(5) NOT NULL AUTO_INCREMENT,
    nom_tableau VARCHAR(255),
    prix_assurance DECIMAL(15,2),
    date_realisation DATE,
    peintre VARCHAR(50),
    localisation_musee VARCHAR(255),
    photo VARCHAR(255),
    mouvement VARCHAR(255),
    type_epoque_id INT(5),
    CONSTRAINT tableau_fk FOREIGN KEY (type_epoque_id) REFERENCES type_epoque(id_type_epoque),
    PRIMARY KEY (id_tableau)
);

INSERT INTO type_epoque (id_type_epoque, libelle)
VALUES (NULL, 'Renaissance'),
       (NULL,'Temps Modernes'),
       (NULL, 'Contemporain'),
       (NULL, 'Moyen-Age');

INSERT INTO tableau (id_tableau, nom_tableau, prix_assurance, date_realisation, peintre, localisation_musee, photo, mouvement, type_epoque_id)
VALUES (NULL, 'La Joconde', 4000, '1506-10-21', 'Léonard de Vinci', 'Louvre', 'laJoconde.jpeg', NULL, 1),
       (NULL, 'Le Radeau de La Méduse', 300.2,'1819-03-15', 'Théodore Géricault', 'Louvre', 'leRadeauDeLaMeduse.jpeg', 'romantisme', 3),
       (NULL, 'Guernica', 200.6,'1937-06-04', 'Pablo Picasso', 'Reina Sofia', 'guernica.jpeg', 'cubisme',3),
       (NULL, 'L Ecole d Athène', 105.3,'1512-02-21', 'Raphaël', 'Vatican', 'lEcoleDAthene.jpeg', 'maniérisme', 1),
       (NULL, 'La Jeune Fille à la perle', 2040,'1665-11-12', 'Johannes Vermeer', 'Mauritshuis', 'laJeuneFilleALaPerle.jpeg', 'baroque',2),
       (NULL, 'La Laitière', 3040,'1658-05-30','Johannes Vermeer', 'Rijksmuseum', 'laLaitière.jpeg', 'baroque', 2),
       (NULL, 'Le Calvaire', 5060,'1505-09-30', 'Josse Lieferinxe', 'Louvre', 'leCalvaire.jpeg', NULL, 1),
       (NULL,'Portrait du bouffon Gonella',1230,'1445-03-18', 'Jean Fouquet', 'Kunsthistorisches Museum', 'leProtraitduBouffonGonella.jpeg', NULL, 4),
       (NULL,'La liberté guidant le peuple', 150.5,'1830-12-25', 'Eugène DelaCroix', 'Louvre', 'laLiberteGuidantlePeuple.jpeg', 'romantisme', 3),
       (NULL,'Rentable de l Agneau mystique', 1010,'1432-01-05', 'Jan van Eyck', 'Cathédrale Saint-Bavon de Gand', 'AgneauMystique.jpeg', NULL, 4);

SELECT * FROM type_epoque;
SELECT * FROM tableau;