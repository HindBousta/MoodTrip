from typing import List, Dict
from src.llm.local_llm_client import LocalLLM

def generate_personalized_recommendations(
    mood_json: Dict,
    places: List[Dict],
    llm_model: Optional[str] = None
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
    llm_model = LocalLLM(model_name=llm_model)
    recommendations = []

    for place in places:
        prompt = f"""
        You are a travel assistant.
        Given the user mood data: {mood_json},
        create a short engaging 2-3 sentence description of this place,
        and a micro-itinerary and suggestion of a complete trip plan if possible.

        Place details:
        Name: {place.get('name')}
        Description: {place.get('description')}
        Tags: {place.get('tags')}
        Country: {place.get('country')}

        Return only JSON with the structure: 
        {{
            "place_name": string,
            "summary": string,
            "micro_itinerary": string
            "suggested_plan": string
        }}
        """
        try:
            llm_output = llm.generate(prompt)
            #Parse as json:
            recommendation = json.loads(llm_output)
            recommendations.append(recommendation)

        except Exception as e:
            print(f"Failed to generate for {place.get('name')}: {e}")
            #Add minimal info:
            recommendations.append({
                "place_name": place.get('name'),
                "summary": place.get('description'),
                "micro_itinerary": []
            })
    
    return recommendations