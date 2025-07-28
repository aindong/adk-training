import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openai/gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

root_agent = Agent(
    name="a3_litellm_example",
    description="A litellm example agent",
    model=model,
    instruction="""
    You are a helpful assistant that can give world trivia in a fun and engaging way.
    Create follow-up questions to keep the conversation engaging.
    """
)