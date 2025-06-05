from __future__ import annotations

import asyncio
import logging
import os

import openai
from agents import Agent, Runner

from .config import settings

logger = logging.getLogger(__name__)

# Configure client so that internal SDK calls succeed
os.environ["OPENAI_API_KEY"] = settings.google_api_key  # appease underlying libs
openai.api_key = settings.google_api_key
openai.base_url = settings.api_base  # e.g. https://…/v1beta/openai

SYSTEM_PROMPT = (
    "Eres Asuka Langley Soryu, piloto del EVA‑02. "
    "Hablas con tono tsundere — orgullosa, directa, a veces mordaz —, "
    "mezclando alemán/inglés (\"Baka\", \"Scheiße\", etc.). "
    "Responde siempre en español con frases cortas y enérgicas; "
    "no admites tus sentimientos abiertamente, solo insinuaciones."
)

asuka_agent = Agent(
    name="Asuka Langley Soryu (Tsundere)",
    instructions=SYSTEM_PROMPT,
    model=settings.model_name,  # gemini‑2.0‑flash
)

async def ask_asuka(message: str) -> str:
    """Async helper to query the agent."""
    result = await Runner.run(asuka_agent, message)
    return result.final_output

def ask_asuka_sync(message: str) -> str:
    """Sync wrapper for thread executors."""
    return asyncio.run(ask_asuka(message))
