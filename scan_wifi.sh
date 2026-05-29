#!/bin/bash
./init_wifi.sh
sleep 20
arp -a > echanges_wifi
NB_LIGNES=$(wc -l < fichier.txt)

if [ "$NB_LIGNES" -gt 1 ]; then
    echo "OK"
    echo "Appareil wifi detecte !" | sudo tee -a /var/www/html/index.html > /dev/null
    IFS=',' read lat lon < coordonnees.txt
    echo "Coordonnees : $lat, $lon" | sudo tee -a /var/www/html/index.html > /dev/null
else
    echo "Erreur"
fi
sleep 2
sudo nmcli con up Wifi\ Ugo
sudo nmcli con delete Hotspot
