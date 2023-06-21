'''Module pour charger le fichier oui.txt et le convertir en dictionnaire'''
from urllib.request import urlopen

def charger_dictionnaire(file):
    """Charge un fichier oui.txt et retourne un dictionnaire avec les cles en 
    minuscules et les valeurs en majuscules"""
    oui = {}
    with open(file, "r", encoding="utf-8") as fichier:
        for line in fichier:
            if "(hex)" in line:
                data = line.split("(hex)")
                key = data[0].lower().strip()
                fabricant = data[1].strip()
                oui[key] = fabricant.upper()
    return oui


def download_oui(to_file):  
    """Telecharge la version actuelle de oui.txt vers le fichier specifie"""
    urloui = "http://standards-oui.ieee.org/oui/oui.txt"
    print(f"Tentative de téléchargement de oui.txt depuis [{urloui}] vers le fichier [{to_file}]")
    oui_data = urlopen(urloui, timeout=10).read()
    with open(to_file, "wb") as oui_file:
        oui_file.write(oui_data)
