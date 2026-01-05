import yaml
from pathlib import Path
from src.utils.path_utils import get_project_root

def load_config() -> dict:
    """
        Load the YAML config file and return it as a Python dictionary
    """
    project_root = get_project_root()
    config_path = project_root / "src" / "config" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path,"r",encoding="utf-8") as f:
        config=yaml.safe_load(f)
    
    return config
    
if __name__=="__main__":
    load_config()   