BASE_URL = "https://www.dominospizza.es/"


class MetaSingleton(type):
    """Metaclass to always make class return the same instance."""

    def __init__(cls, name, bases, attrs):
        super(MetaSingleton, cls).__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MetaSingleton, cls).__call__(*args, **kwargs)

        # Uncomment line to check possible singleton errors
        # logger.info("Requested Connection (id=%d)", id(cls._instance))
        return cls._instance


def remove_accents(string: str) -> str:
    string = string.replace("á", "a")
    string = string.replace("é", "e")
    string = string.replace("í", "i")
    string = string.replace("ó", "o")
    string = string.replace("ú", "u")
    string = string.replace("Á", "A")
    string = string.replace("É", "E")
    string = string.replace("Í", "I")
    string = string.replace("Ó", "O")
    string = string.replace("Ú", "U")
    return string
