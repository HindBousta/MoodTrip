from typing import List, Dict, Optional
import json
from src.llm.local_llm_client import LocalLLM
from src.utils.json_utils import extract_first_json
from src.utils.text_utils import parse_tags
from src.utils.config_loader import load_config

# Load configuration
config = load_config()
DEFAULT_LLM_MODEL = config["interpreter"]["default_model"]

def generate_personalized_recommendations(
    mood_json: Dict,
    places: List[Dict],
    llm_model: str = DEFAULT_LLM_MODEL
) -> List[Dict]:

    """
    Generates personalized travel recommendations and short micro-itineraries
    for each place using local llm

    Args:
        mood_json (Dict): The structured mood Json from MoodInterpreter
        places (List(Dict)): List of top places
        llm_model (str): Local LLM model to use
    Returns: 
        List[Dict]: Each dict contains 'place_name', 'summary', 'micro_itinerary'
    """
    llm = LocalLLM(model_name=llm_model)
    recommendations = []

    for place in places:

        tags = parse_tags(place.get('tags', ''))
        
        prompt = f"""Create personalized travel recommendation for mood: {mood_json['mood']} with tags {mood_json['desired_tags']}

        Place: {place.get('name')}
        {mood_json['mood'].title()} vibe with {', '.join(tags[:3])} tags

        Return ONLY valid JSON:
        {{
        "place_name": "{place.get('name')}",
        "summary": "2-3 sentences about why this matches the mood",
        "micro_itinerary": "1 day plan: Morning->Afternoon->Evening",
        "suggested_plan": "How to get there + best time to visit"
        }}

        JSON:"""

        fallback ={
                "place_name": place.get('name'),
                "summary": place.get('description') or  f"{mood_json['mood'].title()} destination",
                "micro_itinerary": "",
                "suggested_plan": ""
        }

        try:
            response = llm.generate(prompt)
            # Extract only LLM generation (after prompt)
            llm_output = response.strip()

            #Parse as json:
            parsed = extract_first_json(llm_output)
            if parsed is not None:
                recommendations.append(parsed)
            else: 
                recommendations.append(fallback)

        except Exception as e:
            print(f"Failed to generate for {place.get('name')}: {e}")
            #Add minimal info:
            recommendations.append(fallback)
    
    return recommendations