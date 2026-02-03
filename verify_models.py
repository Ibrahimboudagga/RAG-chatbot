import sys
import os

# Add the directory containing the modules to sys.path
# Use strict path to where the files are
sys.path.append(os.path.abspath("src/models/db_schemes/minirag/schemes"))

try:
    from minirag_base import SQLAlchemy_Base
    from project import Project
    from asset import Asset
    from datachunk import DataChunk
    from sqlalchemy import create_engine

    print("Imports successful.")

    engine = create_engine('sqlite:///:memory:')
    SQLAlchemy_Base.metadata.create_all(engine)
    print("Mapping successful.")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)
