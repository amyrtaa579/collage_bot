from typing import Optional
from pydantic import BaseModel

class ApplicationMethod(BaseModel):
    """Модель способа подачи документов"""
    id: Optional[int] = None
    name: str
    description: str
    icon: Optional[str] = None
    display_order: Optional[int] = 0