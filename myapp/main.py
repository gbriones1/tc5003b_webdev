from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from myapp import crud, models, schemas
from myapp.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/user_type/", response_model=schemas.UserTypeSchema)
def create_user_type(user_type: schemas.CreateUserTypeSchema, db: Session = Depends(get_db)):
    db_user_type = crud.create_user_type(db, user_type)
    return db_user_type

@app.get("/user_type/", response_model=List[schemas.UserTypeSchema])
def read_user_types(db: Session = Depends(get_db)):
    return crud.list_user_types(db)

@app.get("/user/", response_model=List[schemas.UserSchema])
def read_users(db: Session = Depends(get_db)):
    users = crud.list_users(db)
    return users

@app.get("/users/{uuid}", response_model=schemas.UserSchema)
def read_user(uuid: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/user/", response_model=schemas.UserSchema)
def create_user(user: schemas.CreateUserSchema, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user

@app.put("/user/{uuid}/", response_model=schemas.UserSchema)
def update_user(uuid: str, user: schemas.UpdateUserSchema, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, uuid, user)
    return db_user

@app.post("/brand/", response_model=schemas.BrandSchema)
def create_brand(brand: schemas.CreateBrandSchema, db: Session = Depends(get_db)):
    db_brand = crud.create_brand(db, brand)
    return db_brand

@app.get("/brand/", response_model=List[schemas.BrandSchema])
def read_brands(db: Session = Depends(get_db)):
    return crud.list_brands(db)

@app.post("/device/", response_model=schemas.DeviceSchema)
def create_device(device: schemas.CreateDeviceSchema, db: Session = Depends(get_db)):
    db_device = crud.create_device(db, device)
    return db_device

@app.get("/device/", response_model=List[schemas.DeviceSchema])
def read_devices(db: Session = Depends(get_db)):
    return crud.list_devices(db)

@app.post("/device_type/", response_model=schemas.DeviceTypeSchema)
def create_device_type(device_type: schemas.CreateDeviceTypeSchema, db: Session = Depends(get_db)):
    db_device_type = crud.create_device_type(db, device_type)
    return db_device_type

@app.get("/device_type/", response_model=List[schemas.DeviceTypeSchema])
def read_device_types(db: Session = Depends(get_db)):
    return crud.list_device_types(db)