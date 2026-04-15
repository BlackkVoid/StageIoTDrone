import time
import serial
import subprocess

ser = serial.Serial('/dev/ttyUSB2', 115200, timeout=1)

def read_ser():
    ser.readline()
    reponse=ser.readline().decode(errors="ignore")
    return reponse

def write_ser(command):
    commande=str(command)
    print(commande)
    true_command=(commande+"\r\n").encode()
    ser.write(true_command)
    time.sleep(0.5)
    reponse=read_ser()
    print(reponse)

def run_bash(command):
    print(command)
    result = subprocess.run(command, shell=True, capture_output>
    print(result.stdout.strip())
    return result.stdout.strip()

write_ser("AT")
print("Configuration de l'interface 4G")
write_ser("AT+CPIN?")
write_ser("AT+CREG?")
write_ser("AT+CGDCONT=1,'IP','sosh'")
write_ser("AT+COPS?")
write_ser("AT+CFUN=0")
write_ser("AT+CFUN=1")

run_bash("sudo ip link set usb0 up")
print("Activation de l'interface 4G")
run_bash("sudo dhclient -r usb0")
print("Initialisation de l'adresse IP")
run_bash("sudo dhclient -v usb0")
print("Connexion 4G activée !")

ser.close()