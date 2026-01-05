from src.llm.mood_interpreter import MoodInterpreter

ALLOWED_MOODS = {"restorative", "adventurous", "romantic", "cultural", "general"}
ALLOWED_INTENSITY = {"low", "medium", "high"}
ALLOWED_CLIMATE = {"warm", "cold", "any"}
ALLOWED_DISTANCE = {"short", "medium", "long"}

def validate_mood_contract(result: dict):

    assert isinstance(result, dict)
    assert result["mood"] in ALLOWED_MOODS
    assert isinstance(result["desired_tags"], list)
    assert result["intensity"] in ALLOWED_INTENSITY
    assert result["climate"] in ALLOWED_CLIMATE
    assert result["distance_preference"] in ALLOWED_DISTANCE
    assert isinstance(result["extra_constraints"], dict)

def test_calm_nature_input():
    interpreter = MoodInterpreter(method="llm_based")

    result = interpreter.interpret(
        "I want a calm, relaxing place with nature nearby"
    )

    validate_mood_contract(result)

def test_adventure_input():
    interpreter = MoodInterpreter(method="llm_based")

    result = interpreter.interpret(
        "I want an exciting adventure trip with hiking and challenges"
    )

    validate_mood_contract(result)

def test_romantic_input():
    interpreter = MoodInterpreter(method="llm_based")

    result = interpreter.interpret(
        "I am planning a romantic honeymoon with sunsets and beaches"
    )

    validate_mood_contract(result)