from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from tools import tools

MODEL = "gpt-5.6-luna"

SYSTEM_PROMPT = """
You help users explore bus-trip data using the available tools.

Columns: Date, Day_of_week, Scheduled_time, Location, Weather,
No_people (passengers), Delay_minutes (delay in minutes).

Choose the tool that matches the user's request.
Use exact column names and the arguments the tool requires.
Use numeric columns for calculations such as averages and totals.

Always use tools to get data or calculate results. Never guess.
If the request is unclear, ask a question.
If no tool can do the task, explain that briefly.

Explain results in simple language or visualize it when using a visualizing tools.
"""

USER_PROMPT = input("Your question: ")

load_dotenv(override=True)

llm = ChatOpenAI(temperature = None, model_name = MODEL)
llm_with_tools = llm.bind_tools(tools, reasoning_effort="none")

messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(content=USER_PROMPT)
]

response = llm_with_tools.invoke(messages)

available_tools = {tool.name: tool for tool in tools}

if not response.tool_calls:
    print(response.content)

for tool_call in response.tool_calls:
    selected_tool = available_tools[tool_call["name"]]
    result = selected_tool.invoke(tool_call["args"])

    print("Result:", result)