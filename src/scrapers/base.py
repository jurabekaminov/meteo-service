import asyncio
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError
from typing import Callable

from httpx import AsyncClient

from src.scrapers.constants import ScraperConstantsEnum


class AbstractScraper(ABC):
    async def __aenter__(self):
        self.__client = AsyncClient(timeout=ScraperConstantsEnum.TIMEOUT.value)
        return self

    async def __aexit__(self, *args):
        await self.__client.aclose()

    @property
    @abstractmethod
    def _headers(self) -> dict[str, str]:
        ...
    async def _get(self, url: str, **kwargs) -> dict:
        return await self.__request(url, self.__client.get, **kwargs)

    async def _post(self, url: str, **kwargs) -> dict:
        return await self.__request(url, self.__client.post, **kwargs)
    
    async def __request(
        self, url: str, method: Callable, retry_counter: int = 0, **kwargs
    ) -> dict:
        response = await method(url, **kwargs)
        try:
            response_json = response.json()
        except JSONDecodeError:
            if retry_counter >= ScraperConstantsEnum.RETRY_ATTEMPTS.value:
                return None
            await asyncio.sleep(ScraperConstantsEnum.WAIT_BETWEEN_RETRIES_SEC.value)
            return await self.__request(url, method, retry_counter + 1, **kwargs)
        return response_json
