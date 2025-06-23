import os
import time
import json
import requests
from bs4 import BeautifulSoup

# ---------------------- FUNCIONES MODULARES ----------------------

def obtener_html(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"❌ Error {response.status_code} al acceder a {url}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la petición: {e}")
        return None

def extraer_nombre_torneo(html):
    soup = BeautifulSoup(html, "html.parser")
    h1 = soup.find("h1")
    if h1:
        return h1.text.strip()
    return "Torneo desconocido"

def extraer_enlaces(html):
    soup = BeautifulSoup(html, "html.parser")
    filas = soup.select("tbody#standings-body tr")
    enlaces = []

    for i, fila in enumerate(filas):
        div_equipo = fila.find("div", class_="team")
        if div_equipo:
            a_tag = div_equipo.find("a")
            if a_tag and a_tag.get("href"):
                enlaces.append(a_tag["href"])
    return enlaces

def guardar_json(data, ruta_salida):
    try:
        with open(ruta_salida, "w") as f:
            json.dump(data, f, indent=4 , ensure_ascii=False)
        print(f"✅ Datos guardados en: {ruta_salida}")
    except IOError as e:
        print(f"❌ Error al guardar el archivo: {e}")

def mostrar_con_pausas(lista, pausa_cada=20, duracion=20):
    for i, enlace in enumerate(lista):
        print(f"[{i+1}] {enlace}")
        if (i + 1) % pausa_cada == 0:
            print(f"⏸ Pausando {duracion} segundos...")
            time.sleep(duracion)

# ---------------------- MAIN ----------------------

def main():
    url = "https://standings.stalruth.dev/2025/special-bologna/masters/"
    ruta_json = ""

    html = obtener_html(url)
    if not html:
        print("❌ No se pudo obtener el HTML.")
        return

    titulo = extraer_nombre_torneo(html)
    enlaces = extraer_enlaces(html)

    if not enlaces:
        print("⚠️ No se encontraron enlaces.")
        return

    mostrar_con_pausas(enlaces)
    
    data = {
        "torneo": titulo,
        "pokepastes": enlaces
    }

    guardar_json(data, ruta_json)

# ---------------------- EJECUCIÓN ----------------------

if __name__ == "__main__":
    main()
