from src.app.generate_trip_suggestions import generate_personalized_recommendations

def generate_trip_suggestions_api(
        user_input: str,
        top_k: int = 3,
        llm_model: Optional[str] = None
) -> List[Dict]:
    """
    API function to generate trip suggestions based on user input.

    Args:
        user_input (str): The user's input describing their mood and preferences.
        top_k (int): The number of top suggestions to return.
        llm_model (Optional[str]): The language model to use for generation.

    Returns:
        List[Dict]: A list of personalized trip suggestions.
    """
    recommendations = generate_personalized_recommendations(
        user_input=user_input,
        top_k=top_k,
        llm_model=llm_model
    )

    return {
        "input": user_input,
        "recommendations": recommendations,
        "count": len(recommendations)
    }