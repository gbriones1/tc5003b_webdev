from typing import List, Union
import time
from datetime import timedelta, datetime

from fastapi import Depends, FastAPI, HTTPException, Response, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from jose import JWTError, jwt
import aioredis

from myapp import crud, models, schemas
from myapp.database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="./myapp/static"), name="static")

templates = Jinja2Templates(directory='./myapp/templates')

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=schemas.Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)

fake_users_db = {
    "user": {
        "username": "user",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/users/me")
async def read_users_me(current_user: schemas.UserSchema = Depends(get_current_user)):
    return current_user

@app.post("/user_type/", response_model=schemas.UserTypeSchema)
def create_user_type(user_type: schemas.CreateUserTypeSchema, db: Session = Depends(get_db)):
    db_user_type = crud.create_user_type(db, user_type)
    return db_user_type

@app.get("/user_type/", response_model=List[schemas.UserTypeSchema])
def read_user_types(db: Session = Depends(get_db)):
    return crud.list_user_types(db)

@app.get("/user/", response_model=List[schemas.UserSchema])
async def read_users(db: Session = Depends(get_db)):
    start = time.time()
    users = crud.list_users(db)
    print(f"Time: {time.time() - start}")
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
def read_devices(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.list_devices(db)

@app.post("/device_type/", response_model=schemas.DeviceTypeSchema)
def create_device_type(device_type: schemas.CreateDeviceTypeSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_device_type = crud.create_device_type(db, device_type)
    return db_device_type

@app.get("/device_type/", response_model=List[schemas.DeviceTypeSchema])
def read_device_types(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.list_device_types(db)

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/devices_list/", response_class=HTMLResponse)
async def devices_list(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("devices.html", {"request": request})