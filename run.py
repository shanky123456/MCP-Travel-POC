import asyncio
from agent import run_query
# from agentWithMultipleMCPServers import run_query

print("starting")
# utterance = input("\n What do you want to do?")
utterance = "Search for Airbnb listings in Mumbai from 20th march 2026 to 22 march 2026 for 2 adults(string) and maxprice as 10000"
asyncio.run(run_query(utterance))  #Utterance will come form tool from bixby --- user_query is actually an utterance which will be coming through Rest API.