import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session(conn_file):

    # read connection data
    with open(conn_file, "r") as f:
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

    return (engine, sessionmaker(bind=engine)())
