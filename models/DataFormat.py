"""
File:    DataFormat.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for data formats

Created on: 2023-06-19
"""

from .meta import *

print("importing module %s" % __name__)


class DataFormat(Base):
    __tablename__ = "data_formats"
    uid: Mapped[int] = mapped_column(primary_key=True)
    format_name: Mapped[str]

    def __repr__(self):
        return "<DataFormat(uid='%s', format_name='%s')>" % (self.uid, self.format_name)
