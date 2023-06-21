import csv
import paho.mqtt.client as mqtt

def envoyer_donnees_mqtt():
    """Envoie les données du fichier CSV via MQTT"""
    # Configuration du broker MQTT
    broker_address = "localhost"  # Adresse IP ou nom d'hôte du Raspberry Pi
    broker_port = 1883  # Port MQTT (par défaut : 1883)

    # Lecture du fichier CSV
    csv_file = '/home/pi/Desktop/ProjetBTS2023/Scan/Donnees/donnees_locales.csv'

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Connexion au broker MQTT
    client = mqtt.Client()
    client.connect(broker_address, broker_port)

    # Publication du fichier CSV
    topic = "donnees_locales"
    payload = '\n'.join(','.join(row) for row in data)
    client.publish(topic, payload)

    # Déconnexion du broker MQTT
    client.disconnect()

    # Affichage du message
    print("Les données ont été envoyées avec succès !")
