import unittest
from transformers import pipeline

class TestModel(unittest.TestCase):
    def test_model_load(self):
        pipe = pipeline("text-generation", model="distilbert-base-uncased")
        self.assertIsNotNone(pipe)

if __name__ == "__main__":
    unittest.main()
