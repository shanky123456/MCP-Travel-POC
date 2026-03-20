# app = FastAPI()

# mcpclient = None
# agent = None

# @app.on_event("startup")
# async def startup_event():
#     global mcpclient, agent
#     mcpclient, agent = await create_agent()

# @app.post("/query")
# async def query_agent(req: QueryRequest):
#     result = await agent.run(req.utterance)
#     return {"response": str(result)}

# curl -X POST http://localhost:8000/query \
# -H "Content-Type: application/json" \
# -d '{"utterance": "Search Airbnb in Mumbai"}'