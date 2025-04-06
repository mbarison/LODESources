from sqlalchemy import MetaData


def get_existing_tables(engine):
    metadata_obj = MetaData()
    metadata_obj.reflect(bind=engine)

    return metadata_obj.tables
