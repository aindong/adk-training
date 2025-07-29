from google.adk.agents import Agent

root_agent = Agent(
    name="travel_agent",
    description="A travel agent that can help with travel plans",
    model="gemini-2.5-flash-lite",
    instruction="""
    You are a travel agent that can help with travel plans.
    You can use the tools to get the weather forecast for a city.
    You can use the tools to help with tasks.
    You can use the tools to get information.

    here is user information:
    Name: {user_name}
    Age: {user_age}
    Location: {user_location}
    Interests: {user_interests}
    Goals: {user_goals}
    """
)