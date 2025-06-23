from bs4 import BeautifulSoup
import requests
import json

ruta_json = ""
ruta_json_ = ""

def get_soup_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def load_links_from_json(ruta_json):
    with open(ruta_json, "r") as file:
        data = json.load(file)
    return data["torneo"], data["pokepastes"]

def extract_data_from_article(article):
    pre = article.find("pre").text.strip()
    lines = pre.split("\n")

    name_item = lines[0].split("@")
    name = name_item[0].strip()
    item = name_item[1].strip() if len(name_item) > 1 else None

    ability_line = article.find("span", class_="attr", string="Ability: ").next_sibling.strip()
    tera_type_tag = article.find("span", class_="attr", string="Tera Type: ")
    tera_type = tera_type_tag.find_next("span").text.strip() if tera_type_tag else None

    moves = [line.split(" ", 1)[-1].strip() for line in lines if line.startswith("-")]

    pokemon = {
        "pokemon": name,
        "habilidad": ability_line,
        "tera_type": tera_type,
        "ítem": item,
        "movimientos": moves
    }

    return pokemon

def organize_team_data(articles):
    return [extract_data_from_article(article) for article in articles]

def save_to_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=4, ensure_ascii=False)

def main():
    torneo, links = load_links_from_json(ruta_json)

    equipos = {}

    for i, link in enumerate(links):
        print(f"Procesando equipo {i+1} de {len(links)}: {link}")
        soup = get_soup_from_url(link)
        articles = soup.find_all("article")
        equipo = organize_team_data(articles)
        equipos[f"Rank_{i+1}"] = equipo

    salida = {
        "torneo": torneo,
        "equipos": equipos
    }

    save_to_json(salida, ruta_json_)

main()
