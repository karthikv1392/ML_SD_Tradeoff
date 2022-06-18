from .db import Base
from sqlalchemy import Column, Integer, Float, DateTime, String


class ServiceStatus(Base):
    __tablename__ = "service_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    cpu_perc = Column(Float)
    service_instance = Column(String(100))
    service_type = Column(String(100))


class LiveServiceStatus(Base):
    __tablename__ = "live_service_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    cpu_perc = Column(Float)
    service_instance = Column(String(100))
    service_type = Column(String(100))


class ServiceCall(Base):
    __tablename__ = "service_call"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    time_delta = Column(Float)
    service_instance = Column(String(100))
    service_type = Column(String(100))


class LiveServiceCall(Base):
    __tablename__ = "live_service_call"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    time_delta = Column(Float)
    service_instance = Column(String(100))
    service_type = Column(String(100))


class Workload(Base):
    __tablename__ = "workloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_init = Column(DateTime)
    ts_end = Column(DateTime)
    days_count = Column(Integer)
    day_duration = Column(Integer)
    label = Column(String(250))
