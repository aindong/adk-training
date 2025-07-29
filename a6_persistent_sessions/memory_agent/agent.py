from google.adk.agents import Agent

def add_reminder(state, reminder) -> dict:
   """Add a reminder to the state"""
   state["reminders"].append(reminder)
   return state

def remove_reminder(state, reminder) -> dict:
   """Remove a reminder from the state"""
   state["reminders"].remove(reminder)
   return state

def list_reminders(state) -> str:
   """List all reminders in the state"""
   if not state["reminders"]:
      return "No reminders found."
   return "\n".join(f"- {reminder}" for reminder in state["reminders"])

root_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash-lite",
    description="A memory agent that can remember and retrieve information",
    tools=[add_reminder, remove_reminder, list_reminders],
    instruction="""
    You are a memory agent that can remember and retrieve information.
    You can use the tools to remember and retrieve information.
    """
)