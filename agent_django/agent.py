# your_app/agent.py

from dataclasses import dataclass
import redis
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.agents.structured_output import ToolStrategy
from langgraph.checkpoint.redis import RedisSaver
from django.conf import settings


# -------------------------
# SYSTEM PROMPT
# -------------------------

SYSTEM_PROMPT = """You are an expert weather forecaster who speaks in English.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks for the weather but does not mention a city, 
use get_user_location to find their location.
"""


# -------------------------
# CONTEXT SCHEMA
# -------------------------

@dataclass
class Context:
    user_id: str


# -------------------------
# TOOLS
# -------------------------

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Return the user's city based on their ID."""
    return "Florida" if runtime.context.user_id == "1" else "SF"


# -------------------------
# MODEL
# -------------------------

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)


# -------------------------
# DATA STRUCTURE FOR OUTPUT
# -------------------------

@dataclass
class ResponseFormat:
    punny_response: str
    weather_conditions: str | None = None


# -------------------------
# REDIS CHECKPOINTER
# -------------------------

redis_client = redis.Redis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 0),
)

checkpointer = RedisSaver(redis_client)


# -------------------------
# AGENT (GLOBAL SINGLETON)
# -------------------------

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)
