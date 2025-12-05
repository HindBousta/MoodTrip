import duckdb
import pandas as pd
from lancedb import connect
from pathlib import Path
from sentence_transformers import SentenceTransformer

from src.utils.config_loader import load_config
from src.utils.path_utils import get_project_root

def build_embeddings(model_name: str | None = None):
    """
    Generates embeddings for all places and stores them in lanceDB vector db

    Args:
        model_name (str | None): Optional embedding model name.
        If None, we use the value default_model in config.yaml
    """

    config = load_config()
    project_root = get_project_root()

    db_path = project_root/ config["paths"]["duckdb_path"]
    lancedb_path = project_root / config["paths"]["lancedb_path"]

    #If model not provided, use default
    if model_name is None:
        model_name = config["embedding"]["default_model"]

    print (f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)

    #Load places from duckDB
    conn = duckdb.connect(str(db_path))
    df = conn.execute("SELECT * FROM places").fetchdf()

    print(f"Loaded {len(df)} places from DB.")

    #Create text for embeddings
    df["embedding_text"] = (
        df["name"]
        + ". " + df["description"].fillna("")
        + ". " + df["tags"].fillna("")
    )

    print(f"Generation embeddings...")
    embeddings = model.encode(df["embedding_text"].tolist(), show_progress_bar = True)

    #Prepare records to insert:
    records = []
    for i, row in df.iterrows():
        records.append({
            "place_id" : row["id"],
            "name" : row["name"],
            "country" : row["country"],
            "category" : row["category"],
            "description" : row["description"],
            "tags" : row["tags"],
            "vector" : embeddings[i].tolist(),
            "model_name" : model_name
        })

    #Connect to lanceDB
    db = connect(str(lancedb_path))

    #Create or open table
    if "places" not in db.table_names():
        table = db.create_table("places", records)
        print("Created LanceDB table 'places'")

    else:
        table = db.open_table("places")
        table.upsert(records)
        print("Updated LanceDB table 'places'")
        
    print(f"Embeddings stored successfully in lanceDB")


if __name__ == "__main__":
    build_embeddings()



