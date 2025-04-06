import pandas as pd


def upload(session, cls, df):
    df.apply(lambda x: session.add(cls(**x)), axis=1)
    session.commit()


def create_and_upload(session, engine, cls, input_file):
    cls.__table__.create(engine)

    df = pd.read_json(input_file, orient="records")

    upload(session, cls, df)
