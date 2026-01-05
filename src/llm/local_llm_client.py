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

    def generate(self, prompt: str, max_new_tokens: int = 120) -> str:
        
        print("Loaded LLM model:", self.model_name)

        print("Encoding prompt...")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: val.to(self.model.device) for key, val in inputs.items()}
        
        print("Generating output...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=0.1,
                top_p=0.1,           # Extreme determinism
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id
            )

        
        print("Decoding output...")
        text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        print("Done")
    
        return text[len(prompt):].strip()