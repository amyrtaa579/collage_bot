import aiohttp
from typing import Optional, List, TypeVar, Generic, Type, Any
from pydantic import BaseModel

from config import settings

T = TypeVar('T', bound=BaseModel)

class APIClient:
    def __init__(self, base_url: str = settings.API_BASE_URL):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _get(self, endpoint: str, params: Optional[dict] = None) -> Any:
        if not self.session:
            self.session = aiohttp.ClientSession()
        url = f"{self.base_url}{endpoint}"
        async with self.session.get(url, params=params) as resp:
            resp.raise_for_status()
            return await resp.json()

    # Методы для публичных эндпоинтов
    async def get_specialties(self, skip: int = 0, limit: int = 50, search: str = None) -> List[dict]:
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        data = await self._get("/college/specialties", params)
        # Ожидаем ответ вида { "success": true, "data": [...] }
        return data.get("data", [])

    async def get_specialty(self, specialty_id: int) -> Optional[dict]:
        data = await self._get(f"/college/specialties/{specialty_id}")
        return data  # предположительно прямой объект

    async def get_specialty_by_code(self, code: str) -> Optional[dict]:
        data = await self._get(f"/college/specialties/code/{code}")
        return data

    async def get_contacts(self) -> List[dict]:
        data = await self._get("/college/contacts")
        return data  # список

    async def get_contact(self, contact_id: int) -> Optional[dict]:
        data = await self._get(f"/college/contacts/{contact_id}")
        return data

    async def get_news(self, limit: int = 10, offset: int = 0) -> List[dict]:
        params = {"limit": limit, "offset": offset}
        data = await self._get("/college/news", params)
        return data

    async def get_news_detail(self, news_id: int) -> Optional[dict]:
        data = await self._get(f"/college/news/{news_id}")
        return data

    async def get_about_sections(self) -> List[dict]:
        data = await self._get("/college/about")
        return data

    async def get_info_section(self, slug: str) -> Optional[dict]:
        data = await self._get(f"/college/info/{slug}")
        return data

    async def get_application_methods(self) -> List[dict]:
        data = await self._get("/college/application-methods")
        return data