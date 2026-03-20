from fastapi import FastAPI
from pydantic import BaseModel
from agentWithMultipleMCPServers import run_query, create_agent

app = FastAPI()

agent = None  # global agent

class QueryRequest(BaseModel):
    utterance: str


@app.on_event("startup")
async def startup_event():
    print("Creating agent once at startup...")
    app.state.agent = await create_agent()
    print("Agent ready 🚀")

@app.post("/query")
async def query_agent(req: QueryRequest):
    try:
        agent = app.state.agent
        response = await run_query(agent, req.utterance)

        return {
            "status": "success",
            "data": response
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }