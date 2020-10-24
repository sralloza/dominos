from pathlib import Path
from typing import List

CODES_PATH = Path(__file__).with_name("codes.txt")


def get_codes() -> List[str]:
    codes = fix_codes()

    codes += [x.lower() for x in codes]
    codes += [x.upper() for x in codes]
    codes = list(set(codes))
    return codes


def fix_codes() -> List[str]:
    codes = CODES_PATH.read_text("utf8").splitlines()
    base_codes = [x.lower().strip() for x in codes if x]
    base_codes = list(set(base_codes))
    base_codes.sort()
    CODES_PATH.write_text("\n".join(base_codes), "utf-8")
    return base_codes
