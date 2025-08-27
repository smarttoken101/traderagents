from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json
import asyncio
from pydantic import BaseModel, Field
from typing import List

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

class AnalysisRequest(BaseModel):
    ticker: str
    analysis_date: str
    analysts: List[str]
    research_depth: int
    llm_provider: str
    shallow_thinker: str
    deep_thinker: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze(request: AnalysisRequest):
    async def event_stream():
        config = DEFAULT_CONFIG.copy()
        config["max_debate_rounds"] = request.research_depth
        config["max_risk_discuss_rounds"] = request.research_depth
        config["quick_think_llm"] = request.shallow_thinker
        config["deep_think_llm"] = request.deep_thinker
        config["llm_provider"] = request.llm_provider.lower()
        if request.llm_provider.lower() == "google":
            config["backend_url"] = "https://generativelanguage.googleapis.com/v1"

        graph = TradingAgentsGraph(request.analysts, config=config, debug=True)

        init_agent_state = graph.propagator.create_initial_state(
            request.ticker, request.analysis_date
        )
        args = graph.propagator.get_graph_args()

        for chunk in graph.graph.stream(init_agent_state, **args):
            if "messages" in chunk and len(chunk["messages"]) > 0:
                last_message = chunk["messages"][-1]
                if hasattr(last_message, "content"):
                    content = str(last_message.content)
                    data = json.dumps({"type": "message", "message": content})
                    yield f"data: {data}\\n\\n"

            for key, value in chunk.items():
                if key != "messages" and value:
                    data = json.dumps({"type": "report", "message": f"<h2>{key}</h2><div>{value}</div>"})
                    yield f"data: {data}\\n\\n"

            await asyncio.sleep(0.1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
