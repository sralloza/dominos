from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dateutil.parser import parse
from unidecode import unidecode

from .codes import get_codes
from .locations import OrderType, Shop, get_shop_by_address
from .networking import Downloader
from .schemas import Address, AppliedPromotion, Information, WorkingCode
from .utils import BASE_URL


class Dominos:
    def __init__(self):
        self.downloader = Downloader()
        self.shop: Optional[Shop] = None
        self.order_type: Optional[OrderType] = None
        self.applied_promotions: List[AppliedPromotion] = []

    def select_shop(self, province, city, street_name, street_number):
        address = Address(
            province=province,
            city=city,
            street_name=street_name,
            street_number=street_number,
        )

        self.shop = get_shop_by_address(address)

    def select_type(self, order_type: str):
        self.order_type = OrderType[order_type]

    def start_order(self):
        payload = {
            "idTienda": self.shop.id,
            "tipoPedido": self.order_type.value.title(),
        }

        url = urljoin(BASE_URL, "Pedido/IniciarPedidoSession")
        response = self.downloader.post(url, data=payload)
        response.raise_for_status()
        assert response.json()["result"] is True

    def check_code(self, code):
        url = urljoin(BASE_URL, "Promocion/AplicarCodPromo")
        payload = {"CodPromo": code, "url": False}

        response = self.downloader.post(url, data=payload)
        response.raise_for_status()

        if not response.json()["result"]:
            return

        url = urljoin(BASE_URL, "promociones")
        response = self.downloader.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        promotions_container = soup.find_all("li", class_="code--promotion")

        for promotion in promotions_container:
            description = promotion["data-name"]
            expires_container = promotion.find("small", class_="small")
            expires_text = unidecode(expires_container.text).strip(" .")
            expires = expires_text.split()[-1].strip(". ")
            expires = parse(expires).date()
            promotion = AppliedPromotion(
                order_type=self.order_type, description=description, expires=expires
            )

            if promotion not in self.applied_promotions:
                self.applied_promotions.append(promotion)
                return WorkingCode(code=code, **promotion.dict())

    def check_all_codes(self):
        codes = get_codes()
        for code in codes:
            code = self.check_code(code)
            if code:
                yield code


def update_codes(addresses: List[Address], base_folder=""):
    if base_folder:
        base_folder = Path(base_folder).absolute()
    else:
        base_folder = Path(__file__).parent.parent

    base_folder.mkdir(exist_ok=True, parents=True)

    for address in addresses:
        dominos = Dominos()
        dominos.select_shop(**address.dict())
        file_path = base_folder / f"{dominos.shop.name_alias}.txt"

        order_types = dict()

        for order_type in OrderType:
            dominos.select_type(order_type.name)
            dominos.start_order()
            codes = []
            for code in dominos.check_all_codes():
                codes.append(code)
            order_types[order_type.value] = codes

        info = Information(
            shop=dominos.shop, updated=datetime.now(), order_types=order_types
        )

        data = info.json(ensure_ascii=False, indent=4)
        file_path.write_text(data, "utf8")
