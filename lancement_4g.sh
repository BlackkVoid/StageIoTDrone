#!/bin/bash
INTERFACE="usb0"

echo "Activation de l'interface $INTERFACE..."
sudo ip link set $INTERFACE up
sleep 2

echo "Obtention d'une adresse IP via DHCP..."
sudo dhclient -v $INTERFACE

IP_ADDR=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
if [ -z "$IP_ADDR" ]; then
    echo "Impossible d'obtenir une IP sur $INTERFACE"
    exit 1
else
    echo "IP obtenue sur $INTERFACE : $IP_ADDR"
fi

echo "Test de la connexion Internet..."
ping -c 4 -I $INTERFACE 8.8.8.8
if [ $? -eq 0 ]; then
    echo "Internet fonctionne via $INTERFACE !"
else
    echo "Échec de la connexion Internet via $INTERFACE"
fi
