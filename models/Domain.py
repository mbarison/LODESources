"""
File:    Domain.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for subject domains

Created on: 2023-06-15
"""

from sqlalchemy.ext.hybrid import hybrid_property


from .meta import Base, Mapped, mapped_column

print("importing module %s" % __name__)


class Domain(Base):
    __tablename__ = "domains"
    domain_uid: Mapped[int] = mapped_column(primary_key=True)
    domain_name_en: Mapped[str]
    domain_name_fr: Mapped[str]

    @hybrid_property
    def domain_name(self) -> str:
        return self.domain_name_en if self.domain_name_en else self.domain_name_fr

    def __repr__(self):
        return "<Domain(domain_uid='%s', domain_name_en='%s', domain_name_fr='%s')>" % (
            self.domain_uid,
            self.domain_name_en,
            self.domain_name_fr,
        )
