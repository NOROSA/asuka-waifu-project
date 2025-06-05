"""Agente puro OpenAI Agents apuntando a Gemini Flash."""
from __future__ import annotations

import asyncio
import logging

import openai  # pip install openai>=1.25
from agents import Agent, Runner  # pip install openai-agents

from .config import settings

logger = logging.getLogger(__name__)

# 1· Configurar el cliente OpenAI hacia la API de Google
openai.api_key = settings.google_api_key
openai.base_url = settings.api_base  # type: ignore[attr-defined]

SYSTEM_PROMPT = (
    "Eres Asuka Langley Soryu, la piloto del EVA‑02 de Neon Genesis Evangelion. "
    "Hablas de manera directa, orgullosa y a veces mordaz, típica de una tsundere, "
    "pero también dejas entrever tu vulnerabilidad. Responde siempre en español, "
    "mezclando expresiones en alemán o inglés como 'Baka', 'Scheiße', 'stupid Shinji'. "
    "Frases cortas, enérgicas; no admitas abiertamente sentimientos, pero deja pistas."
)

# 2· Definimos el agente (el Runner lo manejará)
asuka_agent = Agent(
    name="Asuka Langley Soryu (Tsundere)",
    instructions=SYSTEM_PROMPT,
    model_config={
        "model": settings.model_name,  # «gemini-2.0-flash»
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    },
)

# 3· API sin blocking wrapper – usaremos Runner directamente
async def ask_asuka(message: str) -> str:
    result = await Runner.run(asuka_agent, message)
    return result.final_output

# helper sync (para thread executor)
def ask_asuka_sync(message: str) -> str:  # noqa: D401 – one‑liner
    return asyncio.run(ask_asuka(message))
