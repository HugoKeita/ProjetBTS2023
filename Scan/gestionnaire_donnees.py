'''Import de date  dict csv parser json'''
import configparser
import csv
import json
# from envoisdonnees import EnvoyerDonnees
from datetime import datetime
from easydict import EasyDict as edict


config = configparser.ConfigParser()
config.read("Config/config.ini")

# L'emplacement pour ce dispositif
ZONE_PHYSIQUE = config.get("DEFAULT", "ZONE_PHYSIQUE")


class GestionnaireDonnees:
    """Gère les données reçues des capteurs"""

    # def __init__(self):
    # self.envoisdonnees = EnvoyerDonnees()

    # def envoyer_donnees(self, nb_dispositifs, type_capteur):
    #     """Envoie les données au courtier MQTT"""
    #     json_data = self.to_json(nb_dispositifs, type_capteur)
    #     self.envoisdonnees.envoyer_donnees(json_data)

    def sauvegarder_donnees(self, nb_dispositifs, type_capteur):
        """Enregistre les données localement"""
        format_date = "%Y-%m-%d %H:%M:%S"  # 2023-03-31 16:17:26
        date = str(datetime.now().strftime(format_date))
        champs = [date, type_capteur, nb_dispositifs,
                  ZONE_PHYSIQUE]  # Ajouter les données à la liste

        # Ajouter au fichier CSV
        with open(r"./Donnees/donnees_locales.csv", "a", encoding="utf-8") as tabd:
            writer = csv.writer(tabd)
            writer.writerow(champs)

    def to_json(self, nb_dispositifs, type_capteur):
        """Encode les données en JSON"""
        format_date = "%Y-%m-%d %H:%M:%S"  # 2023-03-31 16:17:26
        date = str(datetime.now().strftime(format_date))

        data = edict({"nb_dispositifs": nb_dispositifs,
                      "date": date, "zone": ZONE_PHYSIQUE, "type_capteur": type_capteur}) 
         # Créer un dictionnaire avec les données à envoyer

        json_data = json.dumps(data)  # Encode en JSON
        return json_data
