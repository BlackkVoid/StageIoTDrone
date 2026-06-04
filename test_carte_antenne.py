#!/usr/bin/env python3
"""
Lance la carte et la réception de données GNSS
"""
import time
import re
import serial
import math
import urllib.request
import subprocess
from io import BytesIO
from PIL import Image

import matplotlib.pyplot as plt

def run_bash(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout.strip())
    return result.stdout.strip()

def nmea_to_decimal(ddmm):
    ddmm = float(ddmm)
    deg = int(ddmm // 100)
    minutes = ddmm - deg * 100
    return deg + minutes / 60

def parse_cgpsinfo(line):

    if not isinstance(line, str):
        return None

    match = re.search(
        r"\+CGPSINFO:\s*([\d.]*),([NS]),([\d.]*),([EW])",
        line
    )

    if not match:
        return None

    lat_raw, ns, lon_raw, ew = match.groups()

    if lat_raw == "" or lon_raw == "":
        return None

    lat = nmea_to_decimal(lat_raw)
    lon = nmea_to_decimal(lon_raw)

    if ns == "S":
        lat = -lat
    if ew == "W":
        lon = -lon

    with open("coordonnees.twt", "w") as f:
      f.write(f"\n{latitude},{longitude}")
    return lat, lon

# ========================
# Récupère les données gps
# ========================
def get_gnss_from_serial(port="/dev/ttyUSB2", baudrate=115200):

    try:
        ser = serial.Serial(port, baudrate, timeout=2)

        ser.write(b"AT+CGPSINFO\r")

        lines = []
        for _ in range(5):
            l = ser.readline().decode(errors="ignore").strip()
            lines.append(l)

        ser.close()

        for l in lines:
            if "+CGPSINFO" in l:
                return parse_cgpsinfo(l)

        return None

    except Exception as e:
        print("Serial error:", e)
        return None


# =========================
# Récupère la carte
# =========================

def deg2num(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2.0 ** zoom

    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)

    return xtile, ytile


def load_osm_tile(lat, lon, zoom=17):

    xtile, ytile = deg2num(lat, lon, zoom)

    url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{zoom}/{ytile}/{xtile}.jpg"

    try:
        img = Image.open(BytesIO(urllib.request.urlopen(url).read()))
        return img
    except Exception as e:
        print("Tile error:", e)
        return None

def get_tile_bounds(lat, lon, zoom):

    xtile, ytile = deg2num(lat, lon, zoom)

    n = 2 ** zoom

    lon_left = xtile / n * 360.0 - 180.0
    lon_right = (xtile + 1) / n * 360.0 - 180.0

    lat_top = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * ytile / n))))
    lat_bottom = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (ytile + 1) / n))))

    return lon_left, lon_right, lat_bottom, lat_top

# =========================
# Affiche la carte
# =========================

def plot_point(lat, lon):

    zoom = 17

    img = load_osm_tile(lat, lon, zoom)

    if img is None:
        print("Erreur tile")
        return

    left, right, bottom, top = get_tile_bounds(lat, lon, zoom)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.imshow(img, extent=[left, right, bottom, top])

    ax.scatter(lon, lat, color="red", s=80, zorder=5)

    ax.set_title("Position du drone")

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # correction affichage
    ax.ticklabel_format(style='plain', useOffset=False)

    coord_text = f"Latitude: {lat:.6f}  |  Longitude: {lon:.6f}"

    ax.text(
        0.5, -0.15, coord_text,
        transform=ax.transAxes,
        ha='center',
        fontsize=10
    )

    plt.tight_layout()
    plt.savefig("/var/www/html/images/CarteFrance.png", dpi=200)

    plt.close(fig)
# =========================
# Main
# =========================

if __name__ == "__main__":

    result = get_gnss_from_serial()

    if result is None:
        print("Pas de fix GPS")
        exit()

    lat, lon = result

    print("GNSS:", lat, lon)

    plot_point(lat, lon)


while True:
    result = get_gnss_from_serial()

    if result:
        lat, lon = result
        plot_point(lat, lon)
        print ("Actualisation !")

    time.sleep(10)

