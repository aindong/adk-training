from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="2_search_agent",
    description="A search agent that can search the web for up to date information",
    model="gemini-2.5-flash-lite",
    instruction="""
    You are a search agent that can search the web for up to date information.
    You can use the following tools: google_search
    """,
    tools=[google_search]
)
