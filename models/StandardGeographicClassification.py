'''
File:    StandardGeographicClassification.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for Standard Geographic Classification

Created on: 2023-06-15
'''

from sqlalchemy.ext.hybrid import hybrid_property

from .meta import *

from .StandardGeographicClassificationLevel import StandardGeographicClassificationLevel 
from .SGCSubType import SGCSubType

print('importing module %s' % __name__)

class StandardGeographicClassification(Base):
    __tablename__ = "standard_geographic_classification"
    dguid = Column(String, primary_key=True)
    sgc_uid: Mapped[str]
    sgc_name_en: Mapped[Optional[str]]
    sgc_name_fr: Mapped[Optional[str]]
    sgc_type_uid: Mapped[int] = mapped_column(ForeignKey(StandardGeographicClassificationLevel.sgc_type_uid))
    sgc_subtype_uid: Mapped[int] = mapped_column()
    __table_args__ = (ForeignKeyConstraint([sgc_type_uid, sgc_subtype_uid], [SGCSubType.sgc_type_uid, SGCSubType.sgc_subtype_uid]),)
    sgc_level = relationship(StandardGeographicClassificationLevel.__name__)
    sgc_subtype = relationship(SGCSubType.__name__, overlaps="sgc_level")

    @hybrid_property
    def sgc_name(self) -> str:
        return self.sgc_name_en if self.sgc_name_en else self.sgc_name_fr

    def __repr__(self):
        return "<StandardGeographicClassification(dguid='%s', sgc_uid='%s', sgc_name_en='%s', sgc_name_fr='%s', sgc_type_uid='%s', sgc_subtype='%s', sgc_level='%s')>" % (
            self.dguid, self.sgc_uid, self.sgc_name_en, self.sgc_name_fr, self.sgc_type_uid, self.sgc_subtype, self.sgc_level)