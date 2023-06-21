#!/bin/bash

# Vérification de la connexion Internet
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
  echo "La connexion Internet est active, on continue le script."
  
  # Mise à jour de pip
  python -m pip install --upgrade pip



  # Installation des dépendances Python
  cd /home/pi/Desktop/ProjetBTS2023
  pip install -r requirements.txt

else
  echo "La connexion Internet est inactive, on arrête le script."
  exit 1
fi
# Build de nexmon
cd /home/pi/Desktop/nexmon-6713f851b56e0bde6383711b56573109d2c0c382
source setup_env.sh
make
# Installation de nexmon
cd /home/pi/Desktop/nexmon-6713f851b56e0bde6383711b56573109d2c0c382/patches/bcm43455c0/7_45_206/nexmon
make
make backup-firmaware
make install-firmware

sleep 2

# Création de l'interface wlan0mon
iw phy `iw dev wlan0 info | gawk '/wiphy/ {printf "phy" $2}'` interface add wlan0mon type monitor
sudo ifconfig wlan0mon up

sleep 2

# Vérification des interfaces réseau
iwconfig
# Activation de l'interface Bluetooth
cd /home/pi/Desktop/ProjetBTS2023/Scan 
sudo hciconfig hci0 up

