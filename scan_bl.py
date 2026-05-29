import asyncio
import subprocess
from bleak import BleakScanner

RSSI_THRESHOLD = -75

def run_bash(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())
    return result.stdout.strip()

async def scan_ble():

    print("Scan Bluetooth en cours...\n")

    while True:

        devices = await BleakScanner.discover(timeout=5.0, return_adv=True)

        nearby_found = False

        for address, (device, adv) in devices.items():

            rssi = adv.rssi if adv.rssi is not None else -100

            if rssi > RSSI_THRESHOLD:

                nearby_found = True
                print("Appareil proche détecté")
                print(f"Nom : {device.name}")
                print(f"MAC : {device.address}")
                print(f"RSSI : {rssi} dBm")
                run_bash("sudo echo 'Un appareil a ete detecte !' | sudo tee -a /var/www/html/index.html > /dev/null")

                run_bash("IFS=',' read lat lon < coordonnees.txt")
                run_bash("sudo echo 'Coordonnees : $lat, $lon' | sudo tee -a /var/www/html/index.html > /dev/null")

                if adv.local_name:
                    print(f"Broadcast Name : {adv.local_name}")

                print("-" * 40)

        if not nearby_found:
            print("Aucun appareil proche")

        await asyncio.sleep(2)

asyncio.run(scan_ble())
