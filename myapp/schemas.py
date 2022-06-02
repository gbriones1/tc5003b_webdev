from typing import List, Optional, Union

from pydantic import BaseModel

class BrandSchema(BaseModel):
    udid: str
    name: str
    
    class Config:
        orm_mode = True

class CreateBrandSchema(BaseModel):
    name: str

class DeviceTypeSchema(BaseModel):
    utid: str
    name: str
    comment: Optional[str]

    class Config:
        orm_mode = True

class CreateDeviceTypeSchema(BaseModel):
    name: str
    comment: str

class DeviceSchema(BaseModel):
    udid: str
    serial_number: str
    description: str
    is_available: bool
    is_outside: bool
    brand: BrandSchema
    device_type: DeviceTypeSchema

    class Config:
        orm_mode = True

class CreateDeviceSchema(BaseModel):
    serial_number: str
    description: Optional[str] = ""
    is_available: bool
    is_outside: bool
    brand_udid: str
    device_type_utid: str

class UserTypeSchema(BaseModel):
    utid: str
    name: str

    class Config:
        orm_mode = True

class CreateUserTypeSchema(BaseModel):
    name: str

class UserSchema(BaseModel):
    uuid: str
    is_manager: bool
    first_name: str
    last_name: str
    email: str
    user_type: UserTypeSchema
    devices: List[DeviceSchema]
    
    class Config:
        orm_mode = True

class CreateUserSchema(BaseModel):
    is_manager: Optional[bool] = False
    first_name: str
    last_name: str
    email: str
    user_type_utid: str

class UpdateUserSchema(BaseModel):
    is_manager: Optional[bool]
    email: Optional[str]
    user_type_utid: Optional[str]
    device_udids: Optional[List[str]] 


class UserSchema(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(UserSchema):
    hashed_password: str
    roles: List[str]

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None