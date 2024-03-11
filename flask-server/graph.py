from sqlalchemy_schemadisplay import create_schema_graph
from sqlalchemy import MetaData
from db_schema import UserData, CompanyData, Articles, FollowedCompanies, Notifications, AffectedCompanies, CompanyWeights, Prediction, HistoricData
import os

def generate_erd(path='erd.png'):
    # Assuming all your SQLAlchemy models are imported and Base is defined
    metadata = MetaData(bind=engine)
    metadata.reflect()

    graph = create_schema_graph(
        metadata=metadata,
        engine=engine,
        show_datatypes=True,  # Show column data types
        show_indexes=True,  # Show index (non-unique)
        rankdir='LR',  # Left to right alignment of tables
        concentrate=False  # Don't join the relation lines together
    )
    graph.write_png(path)  # Write the file to the specified path

if __name__ == '__main__':
    generate_erd('my_database_erd.png')
