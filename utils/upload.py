def upload(sesh, cls, df):
    df.apply(lambda x: sesh.add(cls(**x)), axis=1)
    sesh.commit()
