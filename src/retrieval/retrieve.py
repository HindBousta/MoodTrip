from lancedb import connect
from sentence_transformers import SentenceTransformer
from src.utils.text_utils import parse_tags
import pandas as pd

from src.utils.config_loader import load_config
from src.utils.path_utils import get_project_root

def retrieve_places(query: str, top_k: int = 5, model_name: str = "all-MiniLM-L6-v2") -> pd.DataFrame:
    """
    Retrieve the top_k most similar places to the given query using vector similarity search.

    Args:
        query (str): The input query string.
        top_k (int): The number of top similar places to retrieve.

    Returns:
        pd.DataFrame: A DataFrame containing the top_k similar places.
    """
    # Load configuration
    config = load_config()
    db_path = get_project_root() / config['paths']['lancedb_path']

    # If model name is not provided, use the default from config
    if model_name is None:
        model_name = config['embedding']['default_model']

    print(f"Using embedding model: {model_name}")

    # Load embedding model
    model = SentenceTransformer(model_name)

    # Encode the query into a vector
    qvec = model.encode(query).tolist()

    # Connect to LanceDB
    db = connect(str(db_path))

    #Open table
    table = db.open_table("places")

    # Perform similarity search
    results = (
        table.search(qvec)
        .metric("cosine")
        .limit(top_k)
        .to_pandas()
    )
    # Parse tags from string representation to list
    results["tags"] = results["tags"].apply(parse_tags)

    # Drop the vector column to avoid sending large arrays to generator
    if "vector" in results.columns:
        results = results.drop(columns=["vector"])

    # Add similarity score (higher = more similar)
    results = results.rename(columns={"score": "similarity"})

    return results