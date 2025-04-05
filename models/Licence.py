'''
File:    Licence.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for licences

Created on: 2023-06-19
'''

from meta import *

print('importing module %s' % __name__)

class Licence(Base):
    __tablename__ = "licences"
    uid: Mapped[str] = mapped_column(primary_key=True)
    licence_url: Mapped[str]
    attribution: Mapped[Optional[str]]
    open: Mapped[Optional[str]]
    #xpath: Mapped[Optional[str]]

    def __repr__(self):
        return "<Licence(uid='%s', licence_url='%s', attribution='%s', open='%s')>" % (
            self.uid, self.licence_url, self.attribution, self.open)