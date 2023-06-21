import sys
from datetime import datetime
from scan import Scanner
from gestionnaire_donnees import GestionnaireDonnees
import envoisdonnees  # Import de envoisdonnes.py

def afficher_stats(nb_appareils_wifi, nb_appareils_ble, type_capteur):
    """Affiche le nombre d'appareils trouvés"""
    time = datetime.now().strftime("%H:%M:%S")
    if type_capteur == "Wi-Fi":
        print(time, "| Wi-Fi :", nb_appareils_wifi, "appareils trouvés |", type_capteur)
    elif type_capteur == "Bluetooth":
        print(time, "| Bluetooth :", nb_appareils_ble, "appareils trouvés |", type_capteur)
    else:
        print("Type de capteur inconnu :", type_capteur)


def main():
    """Fonction principale"""
    scanneur = Scanner()
    gestionnaire_donnees = GestionnaireDonnees()

    while True:
        try:
            nb_appareils_ble, nb_appareils_wifi = scanneur.lancer_scan()

            type_capteur = "Wi-Fi"
            afficher_stats(nb_appareils_wifi, nb_appareils_ble, type_capteur)
            gestionnaire_donnees.sauvegarder_donnees(nb_appareils_wifi, type_capteur)

            type_capteur = "Bluetooth"
            afficher_stats(nb_appareils_wifi, nb_appareils_ble, type_capteur)
            gestionnaire_donnees.sauvegarder_donnees(nb_appareils_ble, type_capteur)

        except (KeyboardInterrupt, SystemExit):
            sys.exit()

        # Appel à la fonction d'envoi des données MQTT après les scans
        envoisdonnees.envoyer_donnees_mqtt()

if __name__ == "__main__":
    main()
