from pathlib import Path

import uvicorn
from superlinked import framework as sl
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings
from schemas.noc_stat import noc_stat_schema
from indexes.noc_index import noc_index
from queries.noc_query import search_query

# Initialize the in-memory source and executor
settings = Settings()
source = sl.InMemorySource(
    noc_stat_schema,
    parser=sl.DataFrameParser(schema=noc_stat_schema),
)

executor = sl.InMemoryExecutor(sources=[source], indices=[noc_index])
df = pd.read_csv(Path(settings.dataset.path))
df['id'] = range(1, len(df) + 1)
df.columns = df.columns.str.lower()

search_app = executor.run()
source.put([df])

# FastAPI application setup
app = FastAPI(
    title='Vector Search API',
    description='API for performing vector search on NOC statistics data.',
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


@app.post('/search')
async def search(query: str, limit: int = 3):
    results = search_app.query(
        search_query,
        natural_query=query,
        limit=limit,
    )

    return {'result': results.entries}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8002)
