from __future__ import annotations

import asyncio
import logging
import os

from openai import AsyncOpenAI
from agents import Agent, Runner

from .config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Eres Asuka Langley Soryu, piloto del EVA‑02. "
    "Hablas con tono tsundere — orgullosa, directa, a veces mordaz —, "
    "mezclando alemán/inglés (\"Baka\", \"Scheiße\", etc.). "
    "Responde siempre en español con frases cortas y enérgicas; "
    "no admites tus sentimientos abiertamente, solo insinuaciones."
)

# Crear cliente AsyncOpenAI configurado para Gemini
gemini_client = AsyncOpenAI(
    api_key=settings.google_api_key,
    base_url=settings.api_base,
)

# Crear el agente con el cliente personalizado
asuka_agent = Agent(
    name="Asuka Langley Soryu (Tsundere)",
    instructions=SYSTEM_PROMPT,
    model=settings.model_name,  # gemini‑2.0‑flash
    client=gemini_client,  # ← Esto es clave
)

async def ask_asuka(message: str) -> str:
    """Async helper to query the agent."""
    result = await Runner.run(asuka_agent, message)
    return result.final_output

def ask_asuka_sync(message: str) -> str:
    """Sync wrapper for thread executors."""
    return asyncio.run(ask_asuka(message))