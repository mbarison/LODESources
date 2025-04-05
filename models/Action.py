'''
File:    Action.py
Author:  Marcello Barisonzi CSBP/CPSE <marcello.barisonzi@statcan.gc.ca>

Purpose: ORM model for data retrieval actions

Created on: 2023-06-19
'''

from meta import *

print('importing module %s' % __name__)

class Action(Base):
    __tablename__ = "actions"
    uid: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str]

    def __repr__(self):
        return "<Action(uid='%s', action='%s')>" % (
            self.uid, self.action)