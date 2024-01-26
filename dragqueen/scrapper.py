import logging
import math
import urllib.parse
from itertools import chain

import requests

logger = logging.getLogger("dragqueen")


class Scrapper:
    def __init__(self, base_url, page_size=10):
        self.base_url = base_url
        self.page_size = page_size

    def build_page_query(self, page, page_size=None):
        page_size = page_size or self.page_size
        return (
            self.base_url.rstrip("/")
            + "/api/search/?"
            + urllib.parse.urlencode(
                {"page": page, "page_size": self.page_size, "media_type_in": "pdf"}
            )
        )

    def get_count(self):
        query = self.build_page_query(1, 0)
        return requests.get(query).json()["count"]

    def paginate(self):
        count = self.get_count()
        page_count = math.ceil(count / self.page_size)
        for page in range(1, page_count):
            query = self.build_page_query(page + 1)
            logger.info(f"Grabbing page {page} of {page_count}")
            files = list(
                chain.from_iterable(
                    map(self.process_result, requests.get(query).json()["results"])
                )
            )
            logger.info(f"Received {len(files)} files")
            yield from files

    def process_result(self, item):
        return filter(lambda file: file["media_type"] == "pdf", item["files"])
