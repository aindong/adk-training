import datetime
from google.adk.agents import Agent

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

root_agent = Agent(
    name="1_hello_world_agent",
    model='gemini-2.5-flash-lite',
    description="The hello world agent is a simple agent that says hello world and mentions the current day",
    tools=[get_current_date],
    instruction="""
    You are a helpful assistant that greets the user and mentions the current day and give some random trivia.
    Like this:
    Hello, today is Monday, 28th July 2025.
    You can use the tools to get the current date.
    """,
)
