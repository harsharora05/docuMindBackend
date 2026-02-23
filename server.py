from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI,Query
from .infrastructure.queue import queue
from .workers.query_worker import process_query

app=FastAPI()

@app.post('/chat')
def chat_request(query:str=Query(...,description="The chat query from user")):
    job = queue.enqueue(process_query,query)
    return {"job_id":job.id,"status":"Queued"}


@app.get('/result')
def result(job_id:str = Query(...,description="Job Id")):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"result":result}