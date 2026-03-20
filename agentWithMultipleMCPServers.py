from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from mcp_use import MCPAgent, MCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()


MCP_CONFIG_FILE = "mcpServersNew.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
GEMINI_API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
GEMINI_API_KEY_3 = os.getenv("GEMINI_API_KEY_3")
GEMINI_API_KEY_4 = os.getenv("GEMINI_API_KEY_4")


# llm = ChatOpenAI(model_name="gpt-4o-mini",temperature=0,api_key=OPENAI_API_KEY)                                       ##OpenAI LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,google_api_key=GEMINI_API_KEY_4)                      ##Gemini LLM
async def create_agent():

    with open(MCP_CONFIG_FILE) as f:
        config = json.load(f)


        #initializing client
    print("MCP Configs are : ", config)
    mcpclient = MCPClient.from_dict(config)

    agent = MCPAgent(llm=llm,client=mcpclient, max_steps=8,
    system_prompt="""
    When calling tools:
    - Do NOT include null fields
    """)

    return  agent

async def run_query(agent, utterance: str):
    # agent = await create_agent()

    tool_output = None
    tool_name = None
    tool_input = None
    llm_response = None

    async for step in agent.stream(utterance):
        print("entering here")
        print("step: ", step)
        print("type of step : ", type(step))
        if isinstance(step, (list, tuple)) and len(step) == 2:
            action, tool_output = step
            tool_name = action.tool
            tool_input = action.tool_input
            start = tool_output.find("{")
            end = tool_output.rfind("}") + 1
            data = tool_output[start:end]
            data = data.encode().decode('unicode_escape')
            data = json.loads(data)
            tool_output = data
        elif isinstance(step, str):
            llm_response = step

    print("tool_output : ", tool_output)
    print("llm_response : ", llm_response)

    response = {
    "status": "success",
    "toolName": tool_name,
    "toolInput": tool_input,
    "toolOutput": tool_output,
    "llmResponse" : llm_response
    }

    print("Final Response : ", response)

    return response

