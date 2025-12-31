from typing import List, Dict, Literal, Optional
from src.llm.local_llm_client import LocalLLM
import sys
import re
import json

class MoodInterpreter:
    """
    Converts user's input text into structured mood json data
    Supports rule-based and LLM-based interpretation
    """

    def __init__(self, 
        method: Literal["rule_based", "llm_based"] ="llm_based",
        llm_model: Optional[str] = None,
    ):
        self.method = method
        self.llm_model = llm_model
    
    def interpret(self, user_input: str) -> Dict:
        """
        Interpret user's input into structured mood data        
        Args:
            user_input (str): User's input text describing their mood
        Returns:
            Dict: Structured mood data
        """
        if self.method == "rule_based":
            return self._rule_based(user_input)
        elif self.method == "llm_based":
            return self._llm_based(user_input)
        else:
            raise ValueError(f"Unsupported interpretation method: {self.method}")
        
    #--------------------------
    # Rule-based interpretation
    #--------------------------
    def _rule_based(self, user_input: str) -> Dict:
        """
        Simple rule-based mood interpretation
        """
        text_lower = user_input.lower()
        
        # Map moods
        if any(word in text_lower for word in ["happy", "excited", "adventure", "thrill"]):
            mood = "adventurous"
            tags = ["adventure", "active", "unique"]
        elif any(word in text_lower for word in ["calm", "relax", "rest", "peace"]):
            mood = "restorative"
            tags = ["calm", "nature", "relax"]
        elif any(word in text_lower for word in ["romantic", "love", "couple", "honeymoon"]):
            mood = "romantic"
            tags = ["romantic", "luxury", "sunset"]
        elif any(word in text_lower for word in ["culture", "history", "museum", "temple"]):
            mood = "cultural"
            tags = ["culture", "history", "city", "traditional"]
        else:
            mood = "general"
            tags = []

        # Intensity (simple heuristic)
        intensity = "medium"
        if any(word in text_lower for word in ["very", "extremely", "super"]):
            intensity = "high"
        elif any(word in text_lower for word in ["slightly", "little"]):
            intensity = "low"

        # Climate preference
        if any(word in text_lower for word in ["beach", "sun", "tropical"]):
            climate = "warm"
        elif any(word in text_lower for word in ["snow", "ski", "cold"]):
            climate = "cold"
        else:
            climate = "any"

        # Distance preference
        if any(word in text_lower for word in ["near", "close", "local"]):
            distance_preference = "short"
        elif any(word in text_lower for word in ["far", "remote", "away"]):
            distance_preference = "long"
        else:
            distance_preference = "medium"

        return {
            "mood": mood,
            "desired_tags": tags,
            "intensity": intensity,
            "climate": climate,
            "distance_preference": distance_preference,
            "extra_constraints": {}
        }
    
    #--------------------------
    # LLM-based interpretation
    #--------------------------
    def _llm_based(self, user_input: str) -> Dict:
        """
        LLM-based mood interpretation"""
        if self.llm_model is None:
            llm = LocalLLM()  # use default model
        else:
            llm = LocalLLM(model_name=self.llm_model)

        prompt = f"""
        You are a travel mood interpreter.
        Interpret the following user input into structured mood data:
        User Input: {user_input}

        Return a JSON object with the following structure:
        {{
            "mood":  short label (restorative, adventurous, romantic, cultural, general),
            "desired_tags": [List of relevant tags as strings],
            "intensity": "low|medium|high",
            "climate": "warm|cold|any",
            "distance_preference": "short|medium|long",
            "extra_constraints": any additional constraints as a dictionary
        }}
        Return **only JSON**.

        """
        response = llm.generate(prompt)
        return response
    
if __name__ == "__main__":
    method = sys.argv[1] if len(sys.argv) > 1 else "llm_based"
    interpreter = MoodInterpreter(method=method)
    user_input = "I want a calm, relaxing place with nature nearby"
    mood_json = interpreter.interpret(user_input)
    print(mood_json)