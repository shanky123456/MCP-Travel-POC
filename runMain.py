# import asyncio
# # from agent import run_query
# from agentWithMultipleMCPServers import run_query, create_agent

# print("starting")
# # utterance = "Search for airbnb in mumbai"
# # utterance = "Search for Sports events using ticket master"          #Ticket Master



# utterance = "Search one way flights from BOM airport in Mumbai to BLR airport in Bangalore on 26th march 2026" 
# # utterance = "Search hotels in bangalore from 26th march 2026 to 29th march 2026"
# utterance = "Send message as good to Daddy on whatsapp"
# agent =  asyncio.run(create_agent())
# # asyncio.run(run_query(agent, utterance))  #Utterance will come form tool from bixby --- user_query is actually an utterance which will be coming through Rest API.

# while(True):
#     utterance = input("Enter the utterance: ")
#     asyncio.run(run_query(agent, utterance))


import asyncio
from agentWithMultipleMCPServers import run_query, create_agent

async def main():
    print("starting")

    agent = await create_agent()  # ✅ same loop

    while True:
        utterance = input("Enter the utterance: ")
        await run_query(agent, utterance)  # ✅ no asyncio.run()

if __name__ == "__main__":
    asyncio.run(main())  # ✅ only ONCE    