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

MCP_CONFIG_FILE = "mcpServers.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY_1 = os.getenv("GEMINI_API_KEY_1")
GEMINI_API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
GEMINI_API_KEY_3 = os.getenv("GEMINI_API_KEY_3")
GEMINI_API_KEY_4 = os.getenv("GEMINI_API_KEY_4")


# llm = ChatOpenAI(model_name="gpt-4o-mini",temperature=0,api_key=OPENAI_API_KEY)                                       ##OpenAI LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,google_api_key=GEMINI_API_KEY_1)                      ##Gemini LLM

async def create_agent():

    with open(MCP_CONFIG_FILE) as f:

        config = json.load(f)


        #initializing client
    print("MCP Configs are : ", config)
    mcpclient = MCPClient.from_dict(config)

    agent = MCPAgent(llm=llm,client=mcpclient, max_steps=8)

    return mcpclient, agent

async def extract_param(query):
    messages = [
        SystemMessage(content="Extract the following parameters from the query: location, checkin, checkout, maxprice, adults from supported values are: location: [Mumbai, Delhi, Bangalore], checkin: [YYYY-MM-DD], checkout: [YYYY-MM-DD], maxprice: [integer], adults: [integer] Return only Json object with keys: location, checkin, checkout, maxprice, adults."),
        HumanMessage(content={query})
    ]
    prompt = "what is MCP"
    response  = llm.invoke(prompt)
    print(f"response: {response}")
    return response.content


async def run_query(query:str):
    mcpclient, agent = await create_agent()
    # print("reached here 1")
    # result = await agent.run(query)
    # print("reached here 2")
    # print(f"result: {result}")
    # print("reached here 3")
    #search_args = await extract_param(query)
    #print(f"search args: {search_args}")
   #await mcpclient.connect()
    session = await mcpclient.create_session("ticketmaster")     # session, tool_name and search_args(arguments) should not be hardcoded
                                                            #session - which mcp server to use??
                                                            #tool_name : which tool to use  ---- tobe asked to LLm??
                                                            #search_args : what should be the search_arguments??

    # tool_name = "airbnb_search"
    tool_name = "search_ticketmaster"
    # arguments={
    #         "location": "Mumbai",
    #         "checkin": None,
    #         "checkout":None,
    #         "maxprice": None,
    #         "adults": None
    #     }
    arguments={'type': 'event', 'classificationName' : 'Sports'}   
    print("here1")
    result = await session.call_tool(tool_name,arguments)
    print("result : ", result)
    print("here2")
    raw_result = result.content[0].text


    print("raw_result : ", raw_result)
