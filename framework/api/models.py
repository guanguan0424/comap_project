from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# 通用的API响应模型
class APIResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    code: int = 200


# 用户相关模型
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "user"


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_id: str
    username: str
    role: str


class UserProfileResponse(BaseModel):
    user_id: str
    username: str
    email: str
    role: str
    created_at: datetime
    updated_at: datetime


# 产品相关模型
class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str


class ProductResponse(BaseModel):
    product_id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    created_at: datetime
    updated_at: datetime


# 错误响应模型
class APIErrorResponse(BaseModel):
    success: bool
    message: str
    error_code: str
    details: Optional[dict] = None


class PaginationParams(BaseModel):
    page: int = 1
    size: int = 20
    sort_by: Optional[str] = None
    sort_order: str = "asc"


class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    size: int
    total_pages: int