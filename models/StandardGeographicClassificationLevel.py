'''
File:    StandardGeographicClassificationLevel.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for Standard Geographic Classification Levels

Created on: 2023-06-15
'''

from sqlalchemy.ext.hybrid import hybrid_property


from .meta import *

print('importing module %s' % __name__)

class StandardGeographicClassificationLevel(Base):
    __tablename__ = "sgc_levels"
    #__table_args__ = {'extend_existing': True}
    sgc_type_uid: Mapped[int] = mapped_column(primary_key=True)
    sgc_type_name_en: Mapped[str]
    sgc_type_name_fr: Mapped[str]

    @hybrid_property
    def sgc_type_name(self) -> str:
        return self.sgc_type_name_en if self.sgc_type_name_en else self.sgc_type_name_fr


    def __repr__(self):
        return "<StandardGeographicClassificationLevel(sgc_type_uid='%s', sgc_type_name_en='%s', sgc_type_name_fr='%s')>" % (
            self.sgc_type_uid, self.sgc_type_name_en, self.sgc_type_name_fr)