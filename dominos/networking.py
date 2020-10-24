"""Custom downloader with retries control."""

import logging

import requests

from .exceptions import DownloaderError
from .utils import BASE_URL, MetaSingleton

logger = logging.getLogger(__name__)

NEW_HEADERS = {"User-Agent": "AutoDominos/2.0", "Referer": BASE_URL}


class _settings:
    retries = 5
    timeout = 30


settings = _settings()
del _settings


class Downloader(requests.Session):
    """Downloader with retries control.

    Args:
        silenced (bool, optional): if True, only critical errors are logged.
            Defaults to False.
        retries (int, optional): number of retries for each request. If none,
            it's set to settings.retries. Defaults to None.
    """

    def __init__(self, silenced=False, retries=None):
        self.logger = logging.getLogger(__name__)
        self.retries = retries or settings.retries
        self.timeout = settings.timeout

        if silenced is True:
            self.logger.setLevel(logging.CRITICAL)

        super().__init__()
        self.headers.update(**NEW_HEADERS)

    # pylint: disable=arguments-differ
    def request(self, method, url, retries=None, **kwargs) -> requests.Response:
        """Makes an HTTP request.

        Args:
            method (str): HTTP method of the request.
            url (str): url of the request.
            retries (int): override `Downloader.retries` for this request.
            **kwargs: keyword arguments passed to requests.Session.request.

        Raises:
            DownloaderError: if all retries failed.

        Returns:
            requests.Response: HTTP response.
        """

        self.logger.debug("%s %r", method, url)
        retries = retries or self.retries

        while retries > 0:
            try:
                return super().request(method, url, **kwargs)
            except requests.exceptions.RequestException as exc:
                excname = type(exc).__name__
                retries -= 1
                self.logger.warning(
                    "Catched %s in %s, retries=%s", excname, method, retries
                )

        self.logger.critical("Download error in %s %r", method, url)
        raise DownloaderError("max retries failed.")


downloader = Downloader()
