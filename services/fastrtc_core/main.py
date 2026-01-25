from __future__ import annotations

import uvicorn
from agents.graph_builder import get_compiled_graph
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from streams import ReplyOnPauseStream as Stream

graph = get_compiled_graph()

stream = Stream(
    handler_name='llm_with_waiting_time',
    agent_graph=graph,
)

app = FastAPI(
    title='Phone Calling Agent API',
    description='An AI-powered phone calling agent API using FastRTC',
    docs_url='/docs',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # Frontend URL
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
async def health_check():
    """Health check endpoint to monitor service readiness."""
    try:
        return {
            'status': 'healthy',
            'message': 'Service is ready',
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'message': f"Service initialization failed: {str(e)}",
        }

stream.mount(app, path='/voice')


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # stream.ui.launch()
