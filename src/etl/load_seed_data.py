import duckdb
import pandas as pd
from pathlib import Path
from src.utils.config_loader import load_config
from src.utils.path_utils import get_project_root

def load_seed_data():
    
    """
        Load the CSV file and inserts the data in a duckdb table
    """
    config = load_config()

    #Dynamically detect the project root
    project_root = get_project_root()

    #Define paths: 
    DATA_PATH = project_root / config["paths"]["seed_csv_path"]
    DB_PATH = project_root/ config["paths"]["duckdb_path"]

    print("Loading seed CSV into DuckDB...")

    #Read CSV into pandas:
    df = pd.read_csv(DATA_PATH, sep="|")
    
    #Connect to DuckDB (it will create the DB if it doesn't exist)
    con = duckdb.connect(str(DB_PATH))

    #Create or replace table:
    con.execute("CREATE OR REPLACE TABLE places AS SELECT * FROM df")

    #Check data
    result = con.execute("SELECT COUNT(*) FROM places").fetchone()[0]
    print(f"Loaded {result} rows into 'places' table")

    con.close()

if __name__=="__main__":
    load_seed_data()