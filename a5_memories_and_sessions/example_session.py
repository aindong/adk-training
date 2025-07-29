import uuid
import asyncio
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from travel_agent.agent import root_agent as travel_agent


load_dotenv()

session_service = InMemorySessionService()
async def main():
    initial_state = {
        "user_name": "John",
        "user_age": 30,
        "user_location": "London",
        "user_interests": ["travel", "reading", "cooking"],
        "user_goals": ["travel to Japan", "read 10 books", "cook a new recipe"]
    }

    APP_NAME = "John's Travel Planner"
    USER_ID = "john_doe"

    SESSION_ID = str(uuid.uuid4())
    stateful_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state
    )
    print(f"NEW SESSION CREATED: {SESSION_ID}")

    runner = Runner(
        agent=travel_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part(text="Best places to visit in Japan?")]
    )

    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"Final response: {event.content.parts[0].text}")
        
    print("-------------SESSION EVENT EXPLORATION-------------")
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    print("--------------PRINT FINAL STATE--------------------")
    for key, value in session.state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(main())