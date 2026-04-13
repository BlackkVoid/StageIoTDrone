#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import serial
from pyproj import Transformer
import matplotlib.pyplot as plt
import geopandas as gpd

# =========================
# 1. CONVERSION NMEA
# =========================

def nmea_to_decimal(ddmm):
    """
    Convertit format NMEA DDMM.MMMM → degrés décimaux
    """
    ddmm = float(ddmm)
    deg = int(ddmm // 100)
    minutes = ddmm - deg * 100
    return deg + minutes / 60


def parse_cgpsinfo(line):
    """
    Parse AT+CGPSINFO:
    +CGPSINFO: 4738.167629,N,00659.703404,E,...
    """
    match = re.search(
        r"\+CGPSINFO:\s*([\d.]+),([NS]),([\d.]+),([EW])",
        line
    )

    if not match:
        print("No match")
        return None

    lat_raw, ns, lon_raw, ew = match.groups()

    lat = nmea_to_decimal(lat_raw)
    lon = nmea_to_decimal(lon_raw)

    if ns == "S":
        lat = -lat
    if ew == "W":
        lon = -lon

    return lat, lon


# =========================
# 2. CONVERSION CRS
# =========================

gnss_to_lambert = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:2154",
    always_xy=True
)


def gnss_to_xy(lat, lon):
    x, y = gnss_to_lambert.transform(lon, lat)
    return x, y


# =========================
# 3. LECTURE SERIE (ANTENNE)
# =========================

def get_gnss_from_serial(port="/dev/ttyUSB2", baudrate=115200):
    """
    Lit une trame AT+CGPSINFO depuis l'antenne
    """
    ser = serial.Serial(port, baudrate, timeout=1)

    ser.write(b"AT+CGPSINFO\r")
    ser.readline()
    line = ser.readline().decode(errors="ignore")

    ser.close()
#    print (line)
    return parse_cgpsinfo(line)


# =========================
# 4. CARTE
# =========================

def plot_point(x, y):
    france = gpd.read_file("regions.geojson")
    france = france.to_crs("EPSG:2154")  # IMPORTANT: cohérent avec GNSS
    # enlever uniquement les DOM-TOM (outre-mer)
    france = france[~france["nom"].isin([
        "Guadeloupe",
        "Martinique",
        "Guyane",
        "La Réunion",
        "Mayotte"
    ])]

    fig, ax = plt.subplots(figsize=(10, 10))

    france.plot(ax=ax, color="lightgreen", edgecolor="black", alpha=0.6)

    ax.scatter(x, y, color="red", s=50)

    ax.set_title("Position du drone")
    ax.set_xticks([])
    ax.set_yticks([])
    zoom = 30000  # 10 km

    ax.set_xlim(x - zoom, x + zoom)
    ax.set_ylim(y - zoom, y + zoom)
    fig.savefig('/var/www/html/images/CarteFrance.png', dpi=400)


# =========================
# 5. MAIN
# =========================
if __name__ == "__main__":

    # 🔁 SIMULATION (remplace par get_gnss_from_serial)
#    raw = "+CGPSINFO: 4738.167629,N,00659.703404,E,130426,081747.0,346.9,0,"
    result=get_gnss_from_serial()

    if result is None:
        print("Pas de GPS fix")
        exit()

    lat, lon = result

    print("GNSS (deg):", lat, lon)

    x, y = gnss_to_xy(lat, lon)

    print("Lambert-93:", x, y)

    plot_point(x, y)

