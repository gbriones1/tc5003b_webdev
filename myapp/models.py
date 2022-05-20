from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from myapp.database import Base

class Device(Base):
    __tablename__ = "device"

    udid = Column(String, primary_key=True, index=True)
    serial_number = Column(String)
    description = Column(String)
    is_available = Column(Boolean)
    is_outside = Column(Boolean)
    brand_udid = Column(String, ForeignKey("brand.udid"))
    device_type_utid = Column(String, ForeignKey("device_type.utid"))
    manager_uuid = Column(String, ForeignKey("user.uuid"))
    brand = relationship("Brand", back_populates="devices")
    device_type = relationship("DeviceType", back_populates="devices")
    manager = relationship("User", back_populates="devices")

class Brand(Base):
    __tablename__ = "brand"

    udid = Column(String, primary_key=True, index=True)
    name = Column(String)
    devices = relationship("Device", back_populates="brand")


class DeviceType(Base):
    __tablename__ = "device_type"

    utid = Column(String, primary_key=True, index=True)
    name = Column(String)
    comment = Column(String)
    devices = relationship("Device", back_populates="device_type")

class User(Base):
    __tablename__ = "user"

    uuid = Column(String, primary_key=True, index=True)
    is_manager = Column(Boolean)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    user_type_utid = Column(String, ForeignKey("user_type.utid"))
    devices = relationship("Device", back_populates="manager")
    user_type = relationship("UserType", back_populates="users")

class UserType(Base):
    __tablename__ = "user_type"

    utid = Column(String, primary_key=True, index=True)
    name = Column(String)
    users = relationship("User", back_populates="user_type")