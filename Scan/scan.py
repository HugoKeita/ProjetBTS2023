import subprocess
import sys
import threading
import time
import configparser
import bluetooth
from Wifi.wifi import Wifi
import concurrent.futures

config = configparser.ConfigParser()
config.read("Config/config.ini")

sensor_id = config['DEFAULT']['SENSOR_ID']
DUREE_SCAN = int(config['DEFAULT']['SCAN_EN_SEC'])
adaptateur = config['DEFAULT']['ADAPTATEUR_WIFI']

wifi = Wifi(adaptateur)

class Scanner:
    """Classe qui gère le scan des appareils WiFi et Bluetooth à proximité"""

    def __init__(self):
        self.timestamp_start = None

    def lancer_scan(self):
        """Lance les scans Bluetooth et WiFi en parallèle"""
        print("Utilisation de l'adaptateur", adaptateur, "et scan pendant", DUREE_SCAN, "secondes...")
        self.start_timer(DUREE_SCAN)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futur_bluetooth = executor.submit(self.scanner_dispositifs_bluetooth)
            futur_wifi = executor.submit(self.compter_appareils_wifi)

        resultat_bluetooth = futur_bluetooth.result()
        resultat_wifi = futur_wifi.result()

        self.stop_timer()

        print("\nRésultat du scan Bluetooth :")
        print("Nombre de dispositifs Bluetooth détectés :", resultat_bluetooth)

        print("\nRésultat du scan WiFi :")
        print("Nombre d'appareils WiFi trouvés :", resultat_wifi)

        return resultat_bluetooth, resultat_wifi  # Retourne les résultats des scans

    def scanner_dispositifs_bluetooth(self):
        """Scanne les dispositifs Bluetooth et retourne le nombre de dispositifs détectés"""
        try:
            devices = bluetooth.discover_devices(duration=40, lookup_names=True)
            return len(devices)
        except bluetooth.BluetoothError as e:
            print("Erreur lors du scan Bluetooth :", e)
            return 0

    def compter_appareils_wifi(self):
        """Scan pour les appareils WiFi à proximité et retourne le nombre d'appareils trouvés"""
        try:
            nb_appareils_wifi = wifi.decouvrir_appareils(DUREE_SCAN)
            return nb_appareils_wifi
        except Exception as e:
            print("Erreur lors du scan WiFi :", e)
            return 0

    def start_timer(self, scan_duration):
        """Démarre le minuteur"""
        self.t = threading.Thread(target=self.show_timer, args=(scan_duration,))
        self.t.daemon = True
        self.t.start()  # Démarre le compte à rebours
        self.timestamp_start = time.time()  # Démarre le minuteur

    def stop_timer(self):
        """Arrête le minuteur"""
        self.t.join()  # Arrête le compte à rebours
        timestamp_end = time.time()  # Arrête le minuteur

    def show_timer(self, timeleft):
        """Affiche un minuteur de compte à rebours"""
        total = int(timeleft) * 10
        for i in range(total):
            sys.stdout.write("\r")
            timeleft_string = "%ds" % int((total - i + 1) / 10)
            if (total - i + 1) > 600:
                timeleft_string = "%dmin %ds" % (
                    int((total - i + 1) / 600), int((total - i + 1) / 10 % 60))
            sys.stdout.write("[%-50s] %d%% %15s" % ("=" * int(50.5 * i / total), 101 * i / total, timeleft_string))
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r")
        sys.stdout.flush()
        print("")


if __name__ == "__main__":
    main()
