from typing import Optional
from pydantic import BaseModel

class Specialty(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    professional_activity: Optional[str] = None
    activities: Optional[str] = None
    qualities: Optional[str] = None
    subjects: Optional[str] = None
    entrance_tests: Optional[str] = None

    # Дополнительные поля, если они есть в ответе (например, id, is_active)
    id: Optional[int] = None
    is_active: Optional[bool] = None