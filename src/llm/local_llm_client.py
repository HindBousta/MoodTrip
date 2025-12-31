from transformers import AutoModelForCausalLM, AutoTokenizer
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
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            trust_remote_code=True
        )

    def generate(self, prompt: str, max_new_tokens: int = 300) -> str:
        
        print("Encoding prompt...")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: val.to(self.model.device) for key, val in inputs.items()}
        
        print("Generating output...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=0.0
            )
        
        print("Decoding output...")
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(text)
        print("Done")
        
        #Remove prompt prefix
        if text.startswith(prompt):
            text = text[len(prompt):]

        return text.strip()