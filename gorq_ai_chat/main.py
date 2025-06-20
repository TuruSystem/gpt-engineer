import gradio as gr
from transformers import pipeline, Pipeline
import logging
import sys
from config import Config
import os

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# Model loading with error handling
def load_model():
    try:
        logging.info(f"Loading model: {Config.MODEL_NAME}")
        pipe = pipeline("text-generation", model=Config.MODEL_NAME)
        logging.info("Model loaded successfully.")
        return pipe
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        sys.exit(1)

pipe: Pipeline = load_model()

def chat_fn(message, history):
    try:
        response = pipe(message, max_length=Config.MAX_LENGTH)[0]["generated_text"]
        return response
    except Exception as e:
        logging.error(f"Error during inference: {e}")
        return "[Error: Model could not generate a response.]"

with gr.Blocks(theme=gr.themes.Soft(), title="Gorq AI Chat") as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=120):
            gr.Image("assets/gorqai_logo.png", elem_id="logo", show_label=False, show_download_button=False, height=80)
        with gr.Column(scale=4):
            gr.Markdown("""
            # Gorq AI Chat
            <b>Developed by <a href='https://gorqai.digital' target='_blank'>GorqAiPlatforms</a></b>
            <br>
            <i>Runs locally. Your data stays on your machine.</i>
            <br>
            <small>Model: <code>{}</code></small>
            <hr>
            """.format(Config.MODEL_NAME))
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(type='messages', label="Gorq AI Chatbot", height=400)
            msg = gr.Textbox(label="Your message", placeholder="Type here and press Send...")
            send = gr.Button("Send", variant="primary")
        with gr.Column(scale=1, min_width=220):
            gr.Markdown("""
            ### Welcome to Gorq AI Chat!
            - Start a conversation with our AI.
            - All data is processed locally.
            - [Visit GorqAiPlatforms](https://gorqai.digital)
            <br>
            <hr>
            <small>© 2025 GorqAiPlatforms</small>
            """)

    def respond(user_message, chat_history):
        if chat_history is None:
            chat_history = []
        chat_history.append({"role": "user", "content": user_message})
        bot_message = chat_fn(user_message, chat_history)
        chat_history.append({"role": "assistant", "content": bot_message})
        return "", chat_history

    send.click(respond, [msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gorq AI Chat Platform")
    parser.add_argument('--host', type=str, default=Config.HOST, help='Host to run the server on')
    parser.add_argument('--port', type=int, default=Config.PORT, help='Port to run the server on')
    args = parser.parse_args()
    demo.launch(server_name=args.host, server_port=args.port, show_error=True)
