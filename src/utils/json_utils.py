import json
from typing import Dict
import re

def safe_parse_json(llm_output: str, fallback: Dict) -> Dict:
    """
    Safely parse a string as JSON, falling back to a default dict if parsing fails.

    Args:
        llm_output (str): Raw output from the LLM
        fallback (Dict): Default values if parsing fails
    Returns:
        Dict: Parsed JSON with at least all keys from fallback
    """
    try:
        data = json.loads(llm_output)
        # Ensure all keys exist
        for key in fallback.keys():
            if key not in data:
                data[key] = fallback[key]
        return data
    except json.JSONDecodeError:
        return fallback

def extract_first_json(text: str):
    # Remove markdown wrappers first
    text = re.sub(r'```json\s*', '', text, flags=re.DOTALL)
    text = re.sub(r'```\s*$', '', text, flags=re.DOTALL).strip()
    
    # Try multiple JSON extraction strategies
    patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Balanced braces (handles nested)
        r'\{[\s\S]*?\}'                       # Fallback greedy
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            json_str = match.group().strip()
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                continue
    
    return None
