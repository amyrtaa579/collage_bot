from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class InfoBlock(BaseModel):
    """Модель блока информационного раздела"""
    id: int
    section_id: int
    block_type: str  # paragraph, heading, list, etc.
    title: Optional[str] = None
    content: Dict[str, Any]
    order: int


class InfoSection(BaseModel):
    """Модель информационного раздела"""
    id: int
    slug: str
    title: str
    content: str
    display_order: int
    created_at: datetime
    blocks: List[InfoBlock] = []