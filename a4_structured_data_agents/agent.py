from pydantic import BaseModel, Field
from google.adk.agents import Agent

class WeatherForecast(BaseModel):
    city: str = Field(description="The city for which the weather forecast is requested", default="London")
    temperature: float = Field(description="The temperature in degrees Celsius")
    description: str = Field(description="A brief description of the weather")

def get_weather_forecast(city: str) -> WeatherForecast:
    # integrate with a weather API here
    return WeatherForecast(city=city, temperature=20, description="Sunny")

root_agent = Agent(
    name="a4_structured_data_agents",
    description="A structured data agent that can get the weather forecast for a city and return it in a structured format",
    model="gemini-2.5-flash-lite",
    instruction="""
    You are a helpful assistant that can get the weather forecast for a city and return it in a structured format.
    You can use the tools to get the weather forecast for a city.
    """,
    output_schema=WeatherForecast,
    output_key="weather_forecast"
)