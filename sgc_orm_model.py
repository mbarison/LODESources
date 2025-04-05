# create an ORM model in sqlalchemy

import os, sys, json
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def write_clean_json(df, output_file):
    """Write a dataframe to a json file with clean formatting"""

    # drop picket fence backslashes
    # ref: https://stackoverflow.com/a/64826042 
    with open(output_file, "w", encoding="utf8") as o_f:
        json_str = df.to_json(orient="records") 
        o_f.write(json.dumps(json.loads(json_str), ensure_ascii=False, indent=4))

sys.path.append(os.path.join(os.path.dirname(__file__), "models"))

from models import *

engine = create_engine(r"sqlite:///\\btssce\csbpim1\DEIL\Data\Prod\Projects\DEIL_INFC_Green\4-Collection\GOAT PIPELINE TEST\lode_master_database.sqlite", echo=True)

sesh = sessionmaker(bind=engine)()

print(Base.metadata.tables.keys())

try:
    Base.metadata.drop_all(engine)
    Provider.__table__.drop(engine) 
    DataFormat.__table__.drop(engine)
    Action.__table__.drop(engine)
    Licence.__table__.drop(engine)
except:
    pass

#sys.exit()

def upload(cls, df):
    df.apply(lambda x: sesh.add(cls(**x)), axis=1)

StandardGeographicClassificationLevel.__table__.create(engine)

print(Base.metadata.tables.keys())

df2 = pd.read_json(r"data_sources_catalogue\sgc_levels.json", orient="records")

upload(StandardGeographicClassificationLevel, df2)


StandardGeographicClassification.__table__.create(engine)


# load the data into the ORM model
df = pd.read_json(r"data_sources_catalogue\sgc_consolidated_2021.json", orient="records")

upload(StandardGeographicClassification, df)


Domain.__table__.create(engine)

df3 = pd.read_json(r"data_sources_catalogue\domains.json", orient="records")

upload(Domain, df3)


SGCSubType.__table__.create(engine)

df4 = pd.read_json(r"data_sources_catalogue\sgc_subtypes.json", orient="records")

upload(SGCSubType, df4)

Provider.__table__.create(engine)

# loop over sources
import glob
sources = filter(lambda x: 'centres' not in x, glob.glob(r"data_sources_transformer\output\*\providers.json"))
df5 = pd.DataFrame() 

for s in sources:
    print(s)
    df5 = pd.concat([df5, pd.read_json(s, orient="records").fillna("")], ignore_index=True)

df5 = df5[df5["provider_url"] != ""]

print("Duplicate rows:", len(df5[df5.duplicated(["uid"])]))
df5 = df5.drop_duplicates("uid")

upload(Provider, df5)

write_clean_json(df5, r"data_sources_catalogue\consolidated_providers.json")

DataFormat.__table__.create(engine)

df6 = pd.read_json(r"data_sources_catalogue\data_formats.json", orient="records").fillna("")

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
    df7 = pd.concat([df7, pd.read_json(l, orient="records").fillna("")], ignore_index=True)

df7 = df7[df7["licence_url"] != ""]

print("Duplicate rows:", len(df7[df7.duplicated(["uid"])]))
df7 = df7.drop_duplicates("uid")

write_clean_json(df7, r"data_sources_catalogue\consolidated_licences.json")

upload(Licence, df7)

sesh.commit()


