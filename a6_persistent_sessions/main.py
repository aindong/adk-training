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
   print(
      f"\n-- Running Agent --\n"
   )
   final_response_text = None

   await display_state(
      runner.session_service,
      runner.app_name,
      user_id,
      session_id,
      "State BEFORE processing"
   )

   # Get current state to track changes
   current_session = await runner.session_service.get_session(
      app_name=runner.app_name,
      user_id=user_id,
      session_id=session_id
   )
   current_state = current_session.state.copy()

   try:
      async for event in runner.run_async(
         user_id=user_id,
         session_id=session_id,
         new_message=content
      ):
         response, state_delta = await process_agent_response(event, current_state)
         if response:
            final_response_text = response
         
         # If there are state changes, update the session
         if state_delta:
            await update_session_state(runner, user_id, session_id, current_state, state_delta)
            current_state.update(state_delta)
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

async def process_agent_response(event, current_state):
   """Process the agent's response and handle tool calls"""
   print(f"Event ID: {event.id} Author: {event.author}")
   final_response = None
   state_delta = {}

   if event.is_final_response():
      final_response = event.content.parts[0].text.strip()
      print(f"{final_response}")
   else:
      # Handle tool calls for state updates
      calls = event.get_function_calls()
      if calls:
         state_delta = await handle_tool_calls(calls, current_state)
      # print(event.content)

   return final_response, state_delta

async def handle_tool_calls(tool_calls, current_state):
   """Handle tool calls and return state delta"""
   state_delta = {}
   
   for tool_call in tool_calls:
      tool_name = tool_call.name
      tool_args = tool_call.args

      print(f"Tool call: {tool_name} with args: {tool_args}")
      
      if tool_name == "add_reminder":
         reminder = tool_args.get("reminder", "")
         if "reminders" not in current_state:
            current_state["reminders"] = []
         if "reminders" not in state_delta:
            state_delta["reminders"] = current_state["reminders"].copy()
         state_delta["reminders"].append(reminder)
         print(f"Added reminder: {reminder}")
         
      elif tool_name == "remove_reminder":
         reminder = tool_args.get("reminder", "")
         if "reminders" in current_state and reminder in current_state["reminders"]:
            if "reminders" not in state_delta:
               state_delta["reminders"] = current_state["reminders"].copy()
            state_delta["reminders"].remove(reminder)
            print(f"Removed reminder: {reminder}")
            
      elif tool_name == "list_reminders":
         if "reminders" in current_state and current_state["reminders"]:
            reminders_list = "\n".join(f"- {r}" for r in current_state["reminders"])
            print(f"Current reminders:\n{reminders_list}")
         else:
            print("No reminders found.")
   
   return state_delta

async def update_session_state(runner, user_id, session_id, current_state, state_delta):
   """Update session state using the proper ADK method"""
   try:
      # Merge the current state with the delta
      updated_state = current_state.copy()
      updated_state.update(state_delta)
      
      # Delete the existing session and recreate it with updated state
      await runner.session_service.delete_session(
         app_name=runner.app_name,
         user_id=user_id,
         session_id=session_id
      )
      
      # Create a new session with the same ID and updated state
      await runner.session_service.create_session(
         app_name=runner.app_name,
         user_id=user_id,
         session_id=session_id,
         state=updated_state
      )
      print("Session state updated successfully")
   except Exception as e:
      print(f"Failed to update session state: {e}")

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
