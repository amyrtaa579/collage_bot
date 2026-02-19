from typing import Optional, TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    count: Optional[int] = None

class ApiListResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[List[T]] = None
    count: Optional[int] = None