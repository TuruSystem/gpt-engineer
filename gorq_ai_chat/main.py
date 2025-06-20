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

# Image generation pipeline (Stable Diffusion or similar)
def load_image_model():
    try:
        img_pipe = pipeline("text-to-image", model="stabilityai/stable-diffusion-2")
        logging.info("Image model loaded successfully.")
        return img_pipe
    except Exception as e:
        logging.error(f"Failed to load image model: {e}")
        return None

img_pipe = load_image_model()

# Audio generation pipeline (Nari Lab 1.6B)
def load_audio_model():
    try:
        audio_pipe = pipeline("text-to-audio", model="narilab/narilab-tts-1.6b")
        logging.info("Audio model loaded successfully.")
        return audio_pipe
    except Exception as e:
        logging.error(f"Failed to load audio model: {e}")
        return None

audio_pipe = load_audio_model()

def chat_fn(message, history):
    try:
        response = pipe(message, max_length=Config.MAX_LENGTH)[0]["generated_text"]
        return response
    except Exception as e:
        logging.error(f"Error during inference: {e}")
        return "[Error: Model could not generate a response.]"

def image_fn(prompt):
    if img_pipe is None:
        return None
    try:
        result = img_pipe(prompt)[0]["image"]
        return result
    except Exception as e:
        logging.error(f"Error during image generation: {e}")
        return None

def audio_fn(prompt):
    if audio_pipe is None:
        return None
    try:
        result = audio_pipe(prompt)[0]["audio"]
        return result
    except Exception as e:
        logging.error(f"Error during audio generation: {e}")
        return None

with gr.Blocks(theme=gr.themes.Soft(primary_hue="violet", secondary_hue="blue"), title="Gorq AI Suite") as demo:
    with gr.Row():
        with gr.Column(scale=1, min_width=120):
            gr.Image("assets/gorqai_logo.png", elem_id="logo", show_label=False, show_download_button=False, height=80)
        with gr.Column(scale=4):
            gr.Markdown("""
            # Gorq AI Suite
            <b>by <a href='https://gorqai.digital' target='_blank'>GorqAiPlatforms</a></b>
            <br>
            <i>All-in-one AI: Chat, Images, Audio. Your data stays on your machine.</i>
            <br>
            <small>Text Model: <code>{}</code></small>
            <hr>
            """.format(Config.MODEL_NAME))
    with gr.Tabs():
        with gr.TabItem("Chat"):
            chatbot = gr.Chatbot(type='messages', label="Gorq AI Chatbot", height=400)
            msg = gr.Textbox(label="Your message", placeholder="Type here and press Send...")
            send = gr.Button("Send", variant="primary")
            def respond(user_message, chat_history):
                if chat_history is None:
                    chat_history = []
                chat_history.append({"role": "user", "content": user_message})
                bot_message = chat_fn(user_message, chat_history)
                chat_history.append({"role": "assistant", "content": bot_message})
                return "", chat_history
            send.click(respond, [msg, chatbot], [msg, chatbot])
        with gr.TabItem("Image Generation"):
            img_prompt = gr.Textbox(label="Describe your image", placeholder="A futuristic city at sunset")
            img_btn = gr.Button("Generate Image", variant="primary")
            img_output = gr.Image(label="Generated Image", height=320)
            img_btn.click(image_fn, img_prompt, img_output)
        with gr.TabItem("Audio Generation"):
            audio_prompt = gr.Textbox(label="Describe your audio", placeholder="A calm voice saying 'Welcome to Gorq AI'")
            audio_btn = gr.Button("Generate Audio", variant="primary")
            audio_output = gr.Audio(label="Generated Audio", type="filepath")
            audio_btn.click(audio_fn, audio_prompt, audio_output)
    with gr.Row():
        gr.Markdown("""
        <hr>
        <center>
        <b>GorqAiPlatforms &bull; <a href='https://gorqai.digital' target='_blank'>gorqai.digital</a> &bull; 2025</b>
        </center>
        """)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Gorq AI Suite")
    parser.add_argument('--host', type=str, default=Config.HOST, help='Host to run the server on')
    parser.add_argument('--port', type=int, default=Config.PORT, help='Port to run the server on')
    args = parser.parse_args()
    demo.launch(server_name=args.host, server_port=args.port, show_error=True)
