#!/bin/bash
#ssh secours@IP_RASPBERRY_PI
IP_RASPBERRY="127.0.0.1"
PASSWORD="secours"
if [[ `sshpass -p "$PASSWORD" ssh secours@"$IP_RASPBERRY" "/home/secours/test_chemin.sh python3"` == "N'existe pas" ]]
then
    sshpass -p "$PASSWORD" ssh secours@"IP_RASPBERRY" "sudo apt install python3"
    sshpass -p "$PASSWORD" ssh secours@"IP_RASPBERRY" "pip install flask --break-system-packages"
    sshpass -p "$PASSWORD" ssh secours@"IP_RASPBERRY" "pip install 'numpy==1.24.2' --break-system-packages"
    sshpass -p "$PASSWORD" ssh secours@"IP_RASPBERRY" "pip install 'opencv==4.6' --break-system-packages"
    sshpass -p "$PASSWORD" ssh secours@"IP_RASPBERRY" "pip install bleak --break-system-packages"x
else
    echo "Python existe déjà"
fi
#sudo rm /var/www/html/index.html
#sudo touch /var/www/html/index.html
sudo echo "<html><body><h1>Informations lancement des differentes connexions</h1>" | sudo tee /var/www/html/index.html > /dev/null
#sudo python3 init_4g.py
sleep 3
#sudo ./init_wifi.sh
sleep 3
#sudo ./init_bluetooth.sh
sleep 3
#python3 test_carte_antenne.py &
sleep 3
#sudo python3 ./scan_bl.py &
#sudo python3 ./scan_wifi.sh &
sudo echo "</body></html>" | sudo tee -a /var/www/html/index.html > /dev/null
echo "Lancement complété !"
