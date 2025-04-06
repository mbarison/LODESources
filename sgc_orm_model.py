# create an ORM model in sqlalchemy

from models import (
    Base,
    StandardGeographicClassificationLevel,
    StandardGeographicClassification,
    Domain,
    SGCSubType,
    Provider,
    DataFormat,
    Action,
    Licence,
)
from utils import create_and_upload, create_session, get_existing_tables

engine, sesh = create_session("connect.json")

print(Base.metadata.tables.keys())

# try:
#    Base.metadata.drop_all(engine)
#    Provider.__table__.drop(engine)
#    DataFormat.__table__.drop(engine)
#    Action.__table__.drop(engine)
#    Licence.__table__.drop(engine)
# except:
#    pass

# sys.exit()

classes = {
    StandardGeographicClassificationLevel: "sgc_levels.json",
    SGCSubType: "sgc_subtypes.json",
    StandardGeographicClassification: "sgc_consolidated_2021.json",
    Domain: "domains.json",
    Provider: "consolidated_providers.json",
    DataFormat: "data_formats.json",
    Action: "actions.json",
    Licence: "consolidated_licences.json",
}

existing_tables = get_existing_tables(engine)

try:
    for c, infile in classes.items():
        if c.__tablename__ not in existing_tables.keys():
            create_and_upload(sesh, engine, c, f"data/{infile}")
        else:
            print("Skipping", c.__tablename__)
except:
    sesh.close_all()

sesh.close_all()
