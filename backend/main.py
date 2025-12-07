from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rag.ingest import IngestRequest, process_ingest

app = FastAPI(title="Physical AI Textbook Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Physical AI Robotics Textbook API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ingest")
async def ingest_document(request: IngestRequest):
    try:
        result = await process_ingest(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from rag.query import QueryRequest, SelectedTextQueryRequest, process_query, process_selected_query

@app.post("/query")
async def query_knowledge_base(request: QueryRequest):
    try:
        result = await process_query(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query-selected")
async def query_bse_on_full_context(request: SelectedTextQueryRequest):
    try:
        result = await process_selected_query(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
