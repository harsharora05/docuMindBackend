from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Query, UploadFile
from infrastructure.queue import queue
from workers.query_worker import process_query
from workers.indexing_worker import index_file
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid

app=FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/index')
async def index_request(file: UploadFile):
    unique_filename = f"{uuid.uuid4()}_{file.filename.replace(' ', '_')}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    job = queue.enqueue(index_file, file_path, unique_filename)
    return {"job_id": job.id, "collection": unique_filename}

@app.post('/chat')
def chat_request(
    query: str = Query(..., description="The chat query from user"),
    collection: str = Query(..., description="This is the collection name"),
):
    job =  queue.enqueue(process_query, query, collection)
    return {"job_id": job.id, "status": "Queued"}


@app.get('/result')
def result(job_id: str = Query(..., description="Job Id")):
    job = queue.fetch_job(job_id=job_id)
    result = job.result 
    return {"result": result}