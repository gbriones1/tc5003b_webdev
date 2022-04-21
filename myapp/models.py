from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Device(Base):
    __tablename__ = "device"

    udid = Column(String, primary_key=True, index=True)
    serial_number = Column(String)
    description = Column(String)
    is_available = Column(Boolean)
    is_outside = Column(Boolean)

class Brand(Base):
    __tablename__ = "brand"

    udid = Column(String, primary_key=True, index=True)
    name = Column(String)
    devices = relationship("Device", back_populates="brand")


class DeviceType(Base):
    __tablename__ = "device_type"

    udid = Column(String, primary_key=True, index=True)
    name = Column(String)
    devices = relationship("Device", back_populates="brand")

class User(Base):
    __tablename__ = "user"

    uuid = Column(String, primary_key=True, index=True)
    is_manager = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    devices = relationship("Device", back_populates="manager")

class UserType(Base):
    __tablename__ = "user_type"

    utid = Column(String, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", back_populates="user_type")