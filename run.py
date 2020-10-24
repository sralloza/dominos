from dominos.main import Dominos

dominos = Dominos()
dominos.select_shop("valladolid", "valladolid", "plaza circular", 7)
dominos.select_type("delivery")
dominos.start_order()
for code in dominos.check_all_codes():
    print(code)

# a = get_shop_by_address("burgos", "burgos", "calle condesa mencía", 135)
# a = get_shop_by_address("castellón", "vinaros", "papa luna", 25)
