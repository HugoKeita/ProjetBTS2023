import paho.mqtt.client as mqtt

# Configuration du broker MQTT
broker_address = "localhost"  # Adresse IP ou nom d'hôte du Raspberry Pi
broker_port = 1883  # Port MQTT (par défaut : 1883)

# Emplacement du fichier de sortie
output_file = "/var/lib/mysql-files/messages.csv"

# Fonction callback exécutée lorsqu'un message est reçu
def on_message(client, userdata, message):
    payload = message.payload.decode()
    print(f"Message reçu : {payload}")

    # Enregistrement dans le fichier de sortie
    with open(output_file, 'w') as file:
        file.write(payload)

# Connexion au broker MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(broker_address, broker_port)

# Abonnement au topic
topic = "donnees_locales"
client.subscribe(topic)

# Boucle de réception des messages MQTT
client.loop_forever()
