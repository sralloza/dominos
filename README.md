# Domino's codes finder

Given the shop address, it checks all the known coupons to see if they are valid in that specific shops.

## How to use

```python
from dominos.schemas import Address
from dominos.main import update_codes

addresses = [
    Address(
        province="madrid",
        city="madrid",
        street_name="calle atocha",
        street_number=64,
    )
]

update_codes(addresses, base_folder="dominos-codes")
```
