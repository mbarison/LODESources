from sqlalchemy import Boolean, BigInteger, Column, DateTime, Float, ForeignKey, ForeignKeyConstraint, BigInteger, Integer, String
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from typing import List, Optional

#from geoalchemy2 import Geometry

class Base(DeclarativeBase):
    pass