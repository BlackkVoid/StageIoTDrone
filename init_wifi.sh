#!/bin/bash
sudo apt install nmcli
sudo apt remove hostapd dnsmasq
sudo nmcli dev wifi hotspot ifname wlan0 ssid RaspberryPi0 pass>
sudo nmcli con up Hotspot
sleep 10
sudo nmcli con up preconfigured
sudo nmcli con delete Hotspot
