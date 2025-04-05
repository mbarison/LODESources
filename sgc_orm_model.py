# create an ORM model in sqlalchemy

import os, sys, json
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

from models import *
from utils import upload

# read connection data
with open("connect.json", "r") as f:
    conn_data = json.load(f)

Username = conn_data["Username"]
Password = conn_data["Password"]
Hostname = conn_data["Hostname"]
Port = conn_data["Port"]
Database = conn_data["Database"]

engine = create_engine(
    f"postgresql+psycopg2://{Username}:{Password}@{Hostname}:{Port}/{Database}",
    echo=True,
)

sesh = sessionmaker(bind=engine)()

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

StandardGeographicClassificationLevel.__table__.create(engine)

print(Base.metadata.tables.keys())

df2 = pd.read_json("sgc_levels.json", orient="records")

upload(sesh, StandardGeographicClassificationLevel, df2)


StandardGeographicClassification.__table__.create(engine)


# load the data into the ORM model
df = pd.read_json("sgc_consolidated_2021.json", orient="records")

upload(sesh, StandardGeographicClassification, df)


Domain.__table__.create(engine)

df3 = pd.read_json("domains.json", orient="records")

upload(Domain, df3)


SGCSubType.__table__.create(engine)

df4 = pd.read_json("sgc_subtypes.json", orient="records")

upload(SGCSubType, df4)

sys.exit()

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
