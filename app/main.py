from fastapi import FastAPI
from pydantic import BaseModel
from app.chatbot import responder

app = FastAPI(title="Chatbot Peluquería Patas & Estilo")


class Pregunta(BaseModel):
    mensaje: str



@app.get("/")
def home():
    return {"mensaje": "El chatbot de Patas & Estilo está funcionando 🐾"}


@app.post("/chat")
def chat(pregunta: Pregunta):
    respuesta = responder(pregunta.mensaje)
    return {"respuesta": respuesta}