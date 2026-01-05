from typing import List, Dict, Optional
from src.llm.mood_interpreter import MoodInterpreter
from src.retrieval.retrieve import retrieve_places
from src.llm.generator import generate_personalized_recommendations

def generate_trip_suggestions(
        user_input: str,
        top_k: int = 3,
        llm_model: Optional[str] = None
) -> List[Dict]:
    """
    Full pipeline: interpret user's mood, retrieve relevant places, and generate personalized trip suggestions.

    Args:
        user_input (str): The user's input describing their mood and preferences.
        top_k (int): The number of top suggestions to return.
        llm_model (Optional[str]): The language model to use for generation.

    Returns:
        List[Dict]: A list of personalized trip suggestions.
    """
    # Step 1: Interpret the user's mood and preferences
    mood_interpreter = MoodInterpreter(llm_model=llm_model)
    mood_json = mood_interpreter.interpret(user_input)

    # Step 2: Retrieve relevant places based on the interpreted mood
    query = " ".join([mood_json.get("mood", ""), *mood_json.get("desired_tags", [])])
    places_df = retrieve_places(query, top_k=top_k)
    #Convert DataFrame to list of dicts
    places_list = places_df.to_dict(orient="records")

    # Step 3: Generate personalized recommendations
    recommendations = generate_personalized_recommendations(
        mood_json=mood_json,
        places=places_list,
        llm_model=llm_model
    )

    return recommendations