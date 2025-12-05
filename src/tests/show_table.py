from lancedb import connect
from src.utils.config_loader import load_config
from src.utils.path_utils import get_project_root

# Load config & paths
config = load_config()
project_root = get_project_root()
lancedb_path = project_root / config["paths"]["lancedb_path"]

# Connect to LanceDB
db = connect(str(lancedb_path))

# Open the table
table = db.open_table("places")

# Show first 5 rows
df = table.to_pandas().head()
print(df)
