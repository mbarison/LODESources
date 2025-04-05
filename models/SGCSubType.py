"""
File:    SGCSubType.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for Standard Geographic Classification subtypes

Created on: 2023-06-15
"""

from sqlalchemy.ext.hybrid import hybrid_property

from .meta import Base, Mapped, mapped_column, ForeignKey, Optional, relationship

from .StandardGeographicClassificationLevel import StandardGeographicClassificationLevel

print("importing module %s" % __name__)


class SGCSubType(Base):

    __tablename__ = "sgc_subtype"

    sgc_type_uid: Mapped[int] = mapped_column(
        ForeignKey(StandardGeographicClassificationLevel.sgc_type_uid), primary_key=True
    )
    sgc_subtype_uid: Mapped[int] = mapped_column(primary_key=True)
    sgc_subtype_abbr: Mapped[str]
    sgc_subtype_name_en: Mapped[Optional[str]]
    sgc_subtype_name_fr: Mapped[Optional[str]]
    sgc_type = relationship(StandardGeographicClassificationLevel.__name__)

    @hybrid_property
    def sgc_subtype_name(self) -> str:
        return (
            self.sgc_subtype_name_en
            if self.sgc_subtype_name_en
            else self.sgc_subtype_name_fr
        )

    def __repr__(self):
        return (
            "<SGCSubType(sgc_type_uid='%s', sgc_subtype_uid='%s', sgc_type='%s',  sgc_subtype_name_en='%s', sgc_subtype_name_fr='%s')>"
            % (
                self.sgc_subtype_uid,
                self.sgc_type_uid,
                self.sgc_type,
                self.sgc_subtype_name_en,
                self.sgc_subtype_name_fr,
            )
        )
