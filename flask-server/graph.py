from sqlalchemy import create_engine, MetaData
from sqlalchemy_schemadisplay import create_schema_graph

# Assuming the engine is defined in this script or imported correctly
engine = create_engine('sqlite:///db.sqlite', echo=True)

def generate_erd(output_filename='erd.png'):
    metadata = MetaData()
    metadata.reflect(bind=engine)  # Reflect the tables

    graph = create_schema_graph(
        metadata=metadata,
        show_datatypes=True,  # Shows the datatypes of columns in the diagram.
        show_indexes=True,    # Shows index (non-unique) in the diagram.
        rankdir='LR',         # Left to right alignment of tables
        concentrate=False     # Do not try to join the relation lines together
    )
    graph.write_png(output_filename)  # Write out the diagram as a PNG file

if __name__ == '__main__':
    generate_erd('my_database_erd.png')
