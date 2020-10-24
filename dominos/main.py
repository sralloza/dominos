from collections import namedtuple
from typing import List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from dominos.schemas import AppliedPromotion, WorkingCode

from .codes import get_codes
from .locations import OrderType, Shop, get_shop_by_address
from .networking import Downloader
from .utils import BASE_URL


class Dominos:
    def __init__(self):
        self.downloader = Downloader()
        self.shop: Optional[Shop] = None
        self.order_type: Optional[OrderType] = None
        self.applied_promotions: List[AppliedPromotion] = []

    def select_shop(self, province, city, street_name, street_number):
        self.shop = get_shop_by_address(province, city, street_name, street_number)

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
            expires = (
                promotion.find("small", class_="small").text.split()[-1].strip(".")
            )
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
