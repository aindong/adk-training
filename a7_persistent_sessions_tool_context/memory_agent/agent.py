from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
   """Add a reminder to the state"""
   reminders = tool_context.state.get("reminders", [])
   reminders.append(reminder)

   tool_context.state["reminders"] = reminders

   return {
      "action": "add_reminder",
      "reminder": reminder,
      "message": f"Added reminder: {reminder}"
   }

def remove_reminder(reminder: str, tool_context: ToolContext) -> dict:
   """Remove a reminder from the state"""
   reminders = tool_context.state.get("reminders", [])
   if reminder in reminders:
      reminders.remove(reminder)
      tool_context.state["reminders"] = reminders
      return {
         "action": "remove_reminder",
         "reminder": reminder,
         "message": f"Removed reminder: {reminder}"
      }
      
   return {
      "action": "remove_reminder",
      "reminder": reminder,
      "message": f"Reminder '{reminder}' not found"
   }

def list_reminders(tool_context: ToolContext) -> dict:
   """List all reminders in the state"""
   reminders = tool_context.state.get("reminders", [])
   return {
      "action": "list_reminders",
      "reminders": reminders,
      "message": f"Current reminders:\n{reminders}"
   }

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
    
    The tools have access to the session state through tool context, so they can directly
    read and modify the state. You don't need to worry about state management.
    Just use the appropriate tools based on what the user wants to do.
    """
)