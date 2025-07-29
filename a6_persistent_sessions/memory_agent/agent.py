from google.adk.agents import Agent

def add_reminder(reminder: str) -> str:
   """Add a reminder to the state"""
   return f"Added reminder: {reminder}"

def remove_reminder(reminder: str) -> str:
   """Remove a reminder from the state"""
   return f"Removed reminder: {reminder}"

def list_reminders() -> str:
   """List all reminders in the state"""
   return "Listing all reminders"

root_agent = Agent(
    name="memory_agent",
    model="gemini-2.5-flash-lite",
    description="A memory agent that can remember and retrieve information",
    tools=[add_reminder, remove_reminder, list_reminders],
    instruction="""
    You are a memory agent that can remember and retrieve information.
    You can use the tools to remember and retrieve information.
    
    When the user asks to add a reminder, use the add_reminder tool.
    When the user asks to remove a reminder, use the remove_reminder tool.
    When the user asks to list reminders, use the list_reminders tool.
    
    The state is managed by the session service, so you don't need to worry about state management.
    Just use the appropriate tools based on what the user wants to do.
    """
)