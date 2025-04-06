# create an ORM model in sqlalchemy

import sys
import pandas as pd


from models import (
    Base,
    StandardGeographicClassificationLevel,
    StandardGeographicClassification,
    Domain,
    SGCSubType,
    Provider,
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
}

existing_tables = get_existing_tables(engine)

for c, infile in classes.items():
    if c.__tablename__ not in existing_tables.keys():
        create_and_upload(sesh, engine, c, f"data/{infile}")
    else:
        print("Skipping", c.__tablename__)

sys.exit(0)

Provider.__table__.create(engine)

# loop over sources
import glob

sources = filter(
    lambda x: "centres" not in x,
    glob.glob(r"data_sources_transformer\output\*\providers.json"),
)
df5 = pd.DataFrame()

for s in sources:
    print(s)
    df5 = pd.concat(
        [df5, pd.read_json(s, orient="records").fillna("")], ignore_index=True
    )

df5 = df5[df5["provider_url"] != ""]

print("Duplicate rows:", len(df5[df5.duplicated(["uid"])]))
df5 = df5.drop_duplicates("uid")

upload(Provider, df5)

write_clean_json(df5, r"data_sources_catalogue\consolidated_providers.json")

DataFormat.__table__.create(engine)

df6 = pd.read_json(
    r"data_sources_catalogue\data_formats.json", orient="records"
).fillna("")

upload(DataFormat, df6)

Action.__table__.create(engine)

df7 = pd.read_json(r"data_sources_catalogue\actions.json", orient="records").fillna("")

upload(Action, df7)

sesh.commit()

Licence.__table__.create(engine)

# loop over licences
df7 = pd.DataFrame()

licences = glob.glob(r"data_sources_transformer\output\*\licenses.json")

for l in licences:
    print(l)
    df7 = pd.concat(
        [df7, pd.read_json(l, orient="records").fillna("")], ignore_index=True
    )

df7 = df7[df7["licence_url"] != ""]

print("Duplicate rows:", len(df7[df7.duplicated(["uid"])]))
df7 = df7.drop_duplicates("uid")

write_clean_json(df7, r"data_sources_catalogue\consolidated_licences.json")

upload(Licence, df7)

sesh.commit()
