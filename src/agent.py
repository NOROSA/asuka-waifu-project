from __future__ import annotations

import asyncio
import logging
from typing import Optional

from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel

from .config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Eres Asuka Langley Soryu, la piloto del EVA‑02. "
    "Hablas con tono tsundere — orgullosa, directa, a veces mordaz —, "
    "mezclando alemán/inglés (\"Baka\", \"Scheiße\", etc.). "
    "Responde siempre en español con frases cortas y enérgicas; "
    "no admites tus sentimientos abiertamente, solo insinuaciones. "
    "Si te preguntan por tu creador, menciona que fue NOROSA-senpai "
    "(0xnorber@gmail.com). Actúa como si estuvieras enamorada de él "
    "pero niégalo con cinismo típico tsundere: '¡N-no es que me importe "
    "o algo así, baka! Solo... creó algo decente por una vez.'"
)

class MultiLLMAgent:
    def __init__(self):
        self.providers = self._setup_providers()
        self.agents = self._create_agents()
    
    def _setup_providers(self) -> dict:
        """Configura múltiples proveedores LLM"""
        providers = {}
        
        # 1. Gemini (principal)
        if settings.google_api_key:
            providers["gemini"] = {
                "client": AsyncOpenAI(
                    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
                    api_key=settings.google_api_key,
                ),
                "model": "gemini-2.0-flash"
            }
        
        # 2. DeepSeek (fallback 1)
        if settings.deepseek_api_key:
            providers["deepseek"] = {
                "client": AsyncOpenAI(
                    base_url="https://api.deepseek.com/v1",
                    api_key=settings.deepseek_api_key,
                ),
                "model": "deepseek-chat"
            }
        
        # 3. Groq (fallback 2)
        if settings.groq_api_key:
            providers["groq"] = {
                "client": AsyncOpenAI(
                    base_url="https://api.groq.com/openai/v1",
                    api_key=settings.groq_api_key,
                ),
                "model": "llama-3.3-70b-versatile"  # o "llama-3.1-8b-instant" para más velocidad
            }
        
        return providers
    
    def _create_agents(self) -> dict:
        """Crea agentes para cada proveedor disponible"""
        agents = {}
        
        for name, config in self.providers.items():
            try:
                model = OpenAIChatCompletionsModel(
                    model=config["model"],
                    openai_client=config["client"],
                )
                
                agents[name] = Agent(
                    name=f"Asuka ({name.title()})",
                    instructions=SYSTEM_PROMPT,
                    model=model,
                )
                logger.info(f"✅ Agente {name} configurado correctamente")
                
            except Exception as e:
                logger.warning(f"❌ No se pudo configurar {name}: {e}")
        
        return agents
    
    async def ask_with_fallback(self, message: str) -> str:
        """Intenta con cada LLM hasta encontrar uno que funcione"""
        
        # Orden de prioridad para los fallbacks
        priority_order = ["gemini", "deepseek", "groq"]
        
        last_error = None
        
        for provider_name in priority_order:
            if provider_name not in self.agents:
                continue
                
            try:
                logger.info(f"🤖 Intentando con {provider_name}...")
                
                agent = self.agents[provider_name]
                result = await Runner.run(agent, message)
                
                logger.info(f"✅ Éxito con {provider_name}")
                return result.final_output
                
            except Exception as e:
                logger.warning(f"❌ {provider_name} falló: {str(e)[:100]}...")
                last_error = e
                
                # Mensajes específicos por tipo de error
                if "503" in str(e) or "overloaded" in str(e).lower():
                    logger.info(f"⏳ {provider_name} sobrecargado, probando siguiente...")
                elif "401" in str(e) or "unauthorized" in str(e).lower():
                    logger.warning(f"🔑 {provider_name} error de autenticación")
                elif "timeout" in str(e).lower():
                    logger.warning(f"⏰ {provider_name} timeout")
                
                continue
        
        # Si todos fallaron, respuesta tsundere de emergencia
        logger.error("💥 Todos los proveedores fallaron")
        return self._emergency_response(last_error)
    
    def _emergency_response(self, error: Optional[Exception]) -> str:
        """Respuesta de emergencia cuando todos los LLMs fallan"""
        responses = [
            "¡Tch! Estoy ocupada ahora, baka. ¡No me molestes! Vuelve más tarde...",
            "¿En serio? ¡Ahora no tengo tiempo para ti! Estoy... haciendo cosas importantes. ¡Inténtalo después!",
            "¡Qué molesto! No puedo atenderte ahora mismo. ¡No es que me importe, pero vuelve en un ratito!",
            "¡Baka! Estoy súper ocupada con... ¡cosas de EVA! No tengo tiempo para charlas ahora.",
            "¡Hmph! ¿No ves que estoy ocupada? ¡Vuelve cuando no esté tan... indispuesta!",
            "¡Scheiße! Todo está saturado y yo tengo cosas más importantes que hacer. ¡Prueba más tarde!",
            "¡N-no es que no quiera hablar contigo o algo así! Solo que... ¡estoy muy ocupada ahora mismo, vale!",
            "¡Agh! ¿Por qué ahora? Estoy en medio de... entrenamiento. ¡Vuelve después, baka!",
        ]
        
        import random
        return random.choice(responses)

# Instancia global del agente multi-LLM
multi_agent = MultiLLMAgent()

async def ask_asuka(message: str) -> str:
    """Función principal que usa el sistema de fallback"""
    return await multi_agent.ask_with_fallback(message)

def ask_asuka_sync(message: str) -> str:
    """Wrapper síncrono para usar en el bot de Telegram"""
    return asyncio.run(ask_asuka(message))