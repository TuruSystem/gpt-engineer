from transformers import pipeline
from config import Config

pipe = pipeline("text-generation", model=Config.MODEL_NAME)

def get_model_response(message: str) -> str:
    return pipe(message, max_length=Config.MAX_LENGTH)[0]["generated_text"]
