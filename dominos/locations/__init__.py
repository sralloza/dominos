from dominos.schemas import Address, Coords, OrderType, Shop
from enum import Enum
import json
from collections import namedtuple
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dominos.networking import downloader
from dominos.utils import BASE_URL

json_path = Path(__file__).with_name("provinces-cities-ids.json")


def get_shop_by_address(address: Address):
    data = json.loads(json_path.read_text("utf8"))

    for province_name, province_data in data.items():
        if province_name != address.province:
            continue
        for city_name, city_id in province_data["cities"].items():
            if city_name == address.city:
                return find_closest_shop(
                    province_data["id"],
                    city_id,
                    address.street_name,
                    address.street_number,
                )

    raise RuntimeError()


def find_closest_shop(province_id, city_id, street_name, street_number):
    payload = {
        "idProvincia": province_id,
        "idLocalidad": city_id,
        "calle": street_name,
        "numero": street_number,
        "guardarDireccion": False,
    }

    url = urljoin(BASE_URL, "Tienda/BuscarTiendas")

    response = downloader.post(url, data=payload)
    if response.headers["content-type"].split(";")[0] == "application/json":
        if response.json()["result"] is False:
            raise RuntimeError()

    soup = BeautifulSoup(response.text, "html.parser")
    shop = soup.find("ul", class_="listTiendas").find("li")

    return build_shop_from_soup(shop)


def build_shop_from_soup(soup: BeautifulSoup):
    container = soup.find(class_="fl w50")

    shop_id = int(soup["data-idtienda"])
    title = container.h5.text[7:]
    paragraphs = container.find_all("p")
    phone = int(paragraphs[0].text[10:])
    schedule = paragraphs[1].text[9:]
    types = [OrderType(x["name"]) for x in soup.find_all("button")]

    coords = Coords(lat=float(soup["data-latitude"]), long=float(soup["data-longitude"]))
    return Shop(
        id=shop_id,
        title=title,
        phone=phone,
        schedule=schedule,
        types=types,
        coords=coords,
    )


def get_provinces():
    return json.loads(json_path.read_text("utf8"))


def get_codes():
    url = urljoin(BASE_URL, "Tienda/GetLocalidadesJson")
    provinces = {}
    for province_name, province_id in get_provinces().items():
        response = downloader.post(url, data={"provinciaId": province_id})
        cities = {x["Text"]: x["Value"] for x in response.json()}
        provinces[province_name] = {"id": province_id, "cities": cities}
