from fastapi import FastAPI
from pydantic import BaseModel
from agentWithMultipleMCPServers import run_query, create_agent
import json
from datetime import datetime

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

        output = {
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "input": req.utterance,
            "data": response
        }

        # Save to JSON file
        with open("responses.json", "a") as f:
            json.dump(output, f)
            f.write("\n")   # newline for multiple records

        return output

    except Exception as e:
        error_output = {
            "timestamp": datetime.now().isoformat(),
            "status": "error",
            "input": req.utterance,
            "error": str(e)
        }

        # Save error also
        with open("responses.json", "a") as f:
            json.dump(error_output, f)
            f.write("\n")

        return error_output