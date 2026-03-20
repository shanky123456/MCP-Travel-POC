from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from agentWithMultipleMCPServers import run_query

app = FastAPI()

# Request schema
class QueryRequest(BaseModel):
    utterance: str


@app.post("/query")
async def query_agent(req: QueryRequest):
    try:
        tool_data, llm_response = await run_query(req.utterance)

        return {
            "status": "success",
            "tool_data": tool_data,
            "llm_response": llm_response,
            "source": "agent"
        }

    except Exception as e:
        return {
            "status": "error",
            "tool_data": None,
            "llm_response": str(e),
            "source": "backend"
        }