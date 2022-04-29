import uuid
import time

from sqlalchemy.orm import Session
import aioredis

from myapp import models, schemas

def get_user(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.uuid == uuid).first()

def get_device(db: Session, udid: str):
    return db.query(models.Device).filter(models.Device.udid == udid).first()

async def list_users(db: Session):
    # redis = await aioredis.from_url("redis://localhost")
    # users = await redis.get("users")
    # if users:
    #     return users
    time.sleep(2)
    users = db.query(models.User).all()
    # await redis.set("users", users)
    return users

def list_devices(db: Session):
    return db.query(models.Device).all()

def create_device(db: Session, device: schemas.CreateDeviceSchema):
    db_device = models.Device(udid=str(uuid.uuid4()), **device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def list_brands(db: Session):
    return db.query(models.Brand).all()

def create_brand(db: Session, brand: schemas.CreateBrandSchema):
    db_brand = models.Brand(udid=str(uuid.uuid4()), name=brand.name)
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand

def list_device_types(db: Session):
    return db.query(models.DeviceType).all()

def create_device_type(db: Session, device_type: schemas.CreateDeviceTypeSchema):
    db_device_type = models.DeviceType(utid=str(uuid.uuid4()), name=device_type.name)
    db.add(db_device_type)
    db.commit()
    db.refresh(db_device_type)
    return db_device_type

def list_user_types(db: Session):
    return db.query(models.UserType).all()

def create_user_type(db: Session, user_type: schemas.CreateUserTypeSchema):
    db_user_type = models.UserType(utid=str(uuid.uuid4()), name=user_type.name)
    db.add(db_user_type)
    db.commit()
    db.refresh(db_user_type)
    return db_user_type

def list_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.CreateUserSchema):
    db_user = models.User(uuid=str(uuid.uuid4()), **user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, uuid: str, user: schemas.UpdateUserSchema):
    db_user = get_user(db, uuid)
    if user.is_manager is not None:
        db_user.is_manager = user.is_manager
    if user.email:
        db_user.email = user.email
    if user.user_type_utid:
        db_user.user_type_utid = user.user_type_utid
    if user.device_udids is not None:
        for device_udid in user.device_udids:
            db_device = get_device(db, udid=device_udid)
            db_device.manager_uuid = uuid
            db.add(db_device)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user