#!/bin/bash
#"""""""""""""""""""""""""""""""
#Installation et lancement du point d'accès wifi
#""""""""""""""""""""""""""""""
sudo apt install nmcli
sudo apt remove hostapd dnsmasq
sudo nmcli dev wifi hotspot ifname wlan0 ssid RaspberryPi0 pass RaspberryPi0
sudo nmcli con up Hotspot
sleep 10
sudo nmcli con up preconfigured
sudo nmcli con delete Hotspot
