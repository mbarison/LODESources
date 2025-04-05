"""
File:    Provider.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for data providers

Created on: 2023-06-19
"""

from sqlalchemy.ext.hybrid import hybrid_property

from .meta import Base, Mapped, mapped_column, Optional

print("importing module %s" % __name__)


class Provider(Base):
    __tablename__ = "providers"
    uid: Mapped[str] = mapped_column(primary_key=True)
    provider_name_en: Mapped[Optional[str]]
    provider_name_fr: Mapped[Optional[str]]
    provider_url: Mapped[Optional[str]]
    contact_name: Mapped[Optional[str]]

    @hybrid_property
    def provider_name(self) -> str:
        return self.provider_name_en if self.provider_name_en else self.provider_name_fr

    def __repr__(self):
        return (
            "<Provider(provider_uid='%s', provider_name_en='%s', provider_name_fr='%s', provider_url='%s')>"
            % (
                self.uid,
                self.provider_name_en,
                self.provider_name_fr,
                self.provider_url,
            )
        )
