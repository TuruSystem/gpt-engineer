from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.chat import router as chat_router
from utils.branding import GORQAI_BRAND

app = FastAPI(title="Gorq AI Chat API", description=GORQAI_BRAND["slogan"], version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"brand": GORQAI_BRAND}
