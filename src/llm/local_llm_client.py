from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from src.utils.config_loader import load_config

# Load configuration
config = load_config()
DEFAULT_LLM_MODEL = config["interpreter"]["default_model"]

class LocalLLM:
    """
    Minimal wrapper for local HuggingFace model
    """
    def __init__(self, model_name: str = DEFAULT_LLM_MODEL):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

    def generate(self, prompt: str, max_new_tokens: int = 200) -> str:
        print("Encoding prompt...")
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        print("Generating output...")
        output = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )
        print("Decoding output...")
        text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        print("Done")
        
        #Remove prompt prefix
        return text[len(prompt):].strip()