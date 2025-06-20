import os

class Config:
    MODEL_NAME = os.environ.get("GORQ_MODEL", "Qwen/Qwen1.5-0.5B")
    MAX_LENGTH = int(os.environ.get("GORQ_MAX_LENGTH", 100))
    PORT = int(os.environ.get("GORQ_PORT", 7860))
    HOST = os.environ.get("GORQ_HOST", "0.0.0.0")
