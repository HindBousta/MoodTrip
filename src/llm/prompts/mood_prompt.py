MOOD_INTERPRETER_PROMPT = """
Extract travel mood information. 

Example input:
"I want a calm, relaxing place with nature nearby"

Example output:
{"mood":"restorative","desired_tags":["calm","nature"],"intensity":"medium","climate":"any","distance_preference":"medium","extra_constraints":{}}

Input: %s

Output exactly the JSON object above. No markdown. No explanations. No code. JSON only:
"""
