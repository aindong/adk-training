import asyncio
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types

from memory_agent.agent import root_agent as memory_agent

load_dotenv()

db_url = "sqlite:///sessions.db"
session_service = DatabaseSessionService(db_url)

initial_state = {
   "user_name": "John",
   "reminders": ["buy groceries", "call mom", "book flight"]
}

async def call_agent_async(runner, user_id, session_id, user_input):
   """Call the agent asynchronously with user's input"""
   content = types.Content(
      role="user",
      parts=[types.Part(text=user_input)]
   )
   print(f"\n-- Running Agent --\n")
   final_response_text = None

   await display_state(
      runner.session_service,
      runner.app_name,
      user_id,
      session_id,
      "State BEFORE processing"
   )

   try:
      async for event in runner.run_async(
         user_id=user_id,
         session_id=session_id,
         new_message=content
      ):
         if event.is_final_response():
            final_response_text = event.content.parts[0].text.strip()
            print(f"{final_response_text}")
         else:
            # Tool calls are handled automatically by the ADK framework
            # when using tool context, so we don't need to process them manually
            calls = event.get_function_calls()
            if calls:
               # print to console about the tool call
               for call in calls:
                  print(f"Tool call: {call.name} with args: {call.args}")
                  # print to console about the tool call
                  print(f"Tool call processed: {event.author}")
   except Exception as e:
      print(f"Error: {e}")
      final_response_text = "Sorry, I encountered an error. Please try again."
   
   await display_state(
      runner.session_service,
      runner.app_name,
      user_id,
      session_id,
      "State AFTER processing"
   )

async def display_state(session_service, app_name, user_id, session_id, message):
   """Display the state of the session"""
   session = await session_service.get_session(
      app_name=app_name,
      user_id=user_id,
      session_id=session_id
   )

   print(f"\n-- {message} --\n")
   print(f"State: {session.state}")

async def main():
   APP_NAME = "Reminder App"
   USER_ID = "john_doe"

   existing_session = await session_service.list_sessions(
      app_name=APP_NAME,
      user_id=USER_ID
   )

   if existing_session and len(existing_session.sessions) > 0:
      SESSION_ID = existing_session.sessions[0].id
      print(f"Continuing existing session with ID: {SESSION_ID}")
   else:
      print("No existing session found, creating new one")
      new_session = await session_service.create_session(
         app_name=APP_NAME,
         user_id=USER_ID,
         state=initial_state
      )
      SESSION_ID = new_session.id
      print(f"Created new session with ID: {SESSION_ID}")

   runner = Runner(
      agent=memory_agent,
      app_name=APP_NAME,
      session_service=session_service,
   )

   print(f"Welcome to the Reminder App! You have {len(initial_state['reminders'])} reminders to complete.")
   print(f"Type 'exit' to quit.")

   while True:
      user_input = input("You: ")

      if user_input.lower() == "exit":
         print("Goodbye!")
         break
      
      await call_agent_async(
         runner,
         USER_ID,
         SESSION_ID,
         user_input,
      )

if __name__ == "__main__":
    asyncio.run(main())
