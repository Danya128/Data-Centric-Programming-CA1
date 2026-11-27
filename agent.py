from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from matplotlib.figure import Figure
import gradio as gr

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

load_dotenv(override=True)

llm = ChatOpenAI(temperature = None, model_name = MODEL)
llm_with_tools = llm.bind_tools(tools, reasoning_effort="none")

available_tools = {tool.name: tool for tool in tools}

def chat(message, history):
    messages = (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + history
        + [{"role": "user", "content": message}]
    )
    
    response = llm_with_tools.invoke(messages)
    reply = response.content
    chart = None
    
    for call in response.tool_calls:
        selected_tool = available_tools[call["name"]]
        result = selected_tool.invoke(call["args"])
        if isinstance(result, Figure):
            chart = result
            reply += "Here is your chart\n"
        else:
            reply += str(result) + "\n"
    return reply, chart


with gr.Blocks() as app:
    chart_output = gr.Plot()
    gr.ChatInterface(
        fn=chat,
        additional_outputs=[chart_output],
    )
app.launch()