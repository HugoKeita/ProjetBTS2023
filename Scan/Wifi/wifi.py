import os
import os.path
import subprocess
import sys
from Wifi.oui import charger_dictionnaire, download_oui

class Wifi:
    """Classe pour scanner les réseaux WiFi à proximité"""
    def __init__(self, adaptateur="wlan0mon", proche=True, inclure_adresses_mac_aleatoires=True):
        self.adaptateur = adaptateur
        self.proche = proche
        self.inclure_adresses_mac_aleatoires = inclure_adresses_mac_aleatoires
        self.charger_oui()
        self.tshark = "/usr/bin/tshark"
        self.inclure_adresses_mac_aleatoires = True


    def charger_oui(self):
        """Charge la liste des adresses MAC OUI depuis un fichier."""
        oui_dic = "oui.txt"
        if not os.path.isfile(oui_dic) or not os.access(oui_dic, os.R_OK):
            download_oui(oui_dic)

        oui = charger_dictionnaire(oui_dic)
        if not oui:
            print("Impossible de charger [{}].".format(oui_dic))
            sys.exit(1)
        self.oui_list = oui
        print("Le fichier oui a été chargé correctement.")

    def decouvrir_appareils(self, temps_scan_en_sec):
        """Scan des appareils WiFi à proximité"""

        fichier_dump = "/home/pi/Desktop/test-tmp"

        # Scan avec tshark
        commande_capture = ["tshark", "-i", self.adaptateur, "-a", "duration:" + str(temps_scan_en_sec), "-w", fichier_dump, "-q"]

        try:
            process_capture = subprocess.Popen(commande_capture, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            process_capture.communicate()  # Attend la fin de la capture
        except subprocess.CalledProcessError as e:
            print("Erreur lors de la capture des paquets Wi-Fi :", e)
            return

        # Analyse du fichier de capture pour extraire les adresses MAC, puissances de signal et adresses MAC des points d'accès Wi-Fi (BSSID)
        commande_extraction = ["tshark", "-r", fichier_dump, "-T", "fields", "-e", "wlan.sa", "-e", "wlan.bssid", "-e", "radiotap.dbm_antsignal", "-q"]
        try:
            process_extraction = subprocess.Popen(commande_extraction, stdout=subprocess.PIPE)
            sortie, _ = process_extraction.communicate()
        except subprocess.CalledProcessError as e:
            print("Erreur lors de l'extraction des adresses MAC et des puissances de signal :", e)
            return


        found_mac_addresses = set()
        for line in sortie.decode("utf-8").split("\n"):
            if not line.strip():
                continue
            mac = line.split()[0].strip().split(",")[0]
            dats = line.split()
            if len(dats) == 3 and ":" in dats[0]:
                found_mac_addresses.add(mac)

        if not found_mac_addresses:
            print("Aucun signal trouvé. Assurez-vous que {} supporte le mode monitor.".format(self.adaptateur))
            return 0

        # Using get_fabricants_connus method
        fabricants_connus = self.get_fabricants_connus()
        sorted_mac_addresses = sorted(found_mac_addresses, key=lambda mac: self.oui_list.get(mac[:8], 'Pas dans OUI') in fabricants_connus)

        nb_personnes = len(sorted_mac_addresses)

        print("\nLe nombre d'appareils trouvés est de : {}".format(nb_personnes))

        print("\nAdresses MAC triées :")
        adresses_mac_filtrees = [(mac, self.oui_list.get(mac[:8], 'Pas dans OUI')) for mac in sorted_mac_addresses if any(f in self.oui_list.get(mac[:8], 'Pas dans OUI').upper() for f in fabricants_connus) or (self.oui_list.get(mac[:8], 'Pas dans OUI') == 'Pas dans OUI' and self.inclure_adresses_mac_aleatoires)]
        for adresse_mac, fabricant in adresses_mac_filtrees:
            print("Adresse MAC : {}, Fabricant : {}".format(adresse_mac, fabricant))
        nb_personnes_trié = len(adresses_mac_filtrees)
        return nb_personnes_trié


    @staticmethod
    def get_fabricants_connus():
        """Retourne une liste de fabricants de smartphones connus"""
        fabricants_connus = [
            "MOTOROLA",
            "OPPO",
            "HUAWEI",
            "MICROSOFT",
            "HTC",
            "SAMSUNG",
            "BLACKBERRY",
            "APPLE",
            "LG",
            "ONEPLUS",
            "XIAOMI",
            "GOOGLE",
            "ZTE",
            "HMD GLOBAL",
            "FUJITSU",
            "NOKIA",
            "SONY",
            "TCL",
            "VIVO",
            "GIONEE",
            "MEIZU",
            "POCO"
        ]
        return fabricants_connus

    @staticmethod
    def get_adresses_mac_aleatoires_connues():
        """Retourne une liste de préfixes d'adresses MAC aléatoires connus"""
        adresses_mac_aleatoires_connues = ["da:a1:19", "92:68:c3"]
        return adresses_mac_aleatoires_connues
