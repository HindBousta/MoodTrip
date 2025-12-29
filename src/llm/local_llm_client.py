from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LocalLLM:
    """
    Minimal wrapper for local HuggingFace model
    """
    def __init__(self, model_name: str ="TheBloke/vicuna-7B-1.1-HF"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto"
        )

    def generate(self, prompt: str, max_new_tokens: int = 150) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        output = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )
        text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        #Remove prompt prefix
        return text[len(prompt):].strip()