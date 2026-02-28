# 🚀 DocuMind – Async RAG Pipeline

DocuMind is a fully asynchronous **Retrieval-Augmented Generation (RAG)** system built from scratch to explore scalable GenAI system design.

Instead of directly calling an LLM synchronously, this system uses a **job-based async architecture** powered by queues and background workers.

---

# 🏗️ Architecture Overview

## 🔄 Request Flow

1. User sends request to `/chat`
2. API enqueues job in **Valkey (Redis-compatible)**
3. Worker processes:
   - Convert query → embeddings
   - Perform similarity search in **Qdrant**
   - Prepare contextual prompt
   - Call OpenAI LLM
4. Store result in Valkey
5. Client polls `/result/{job_id}`

---

## ✅ Why This Architecture?

- Scalable
- Prevents request timeouts
- Clean separation of API & heavy LLM tasks
- Production-ready async workflow
- Queue-based background processing

---

# 🛠️ Tech Stack

- ⚡ **FastAPI** – Backend API  
- 🔴 **Valkey (Redis-compatible)** – Queue + Result Store  
- 🔁 **RQ (Redis Queue)** – Background workers  
- 🧠 **Qdrant** – Vector database  
- 🤖 **OpenAI API** – Embeddings + LLM  

---


# 🐳 Running with Docker Compose

Make sure you are in the root directory (where `docker-compose.yml` exists).

Start services:

```bash
docker compose up -d
```
Stop services:

```bash
docker compose down
```

## 🔐 Environment Variables

Create a .env file in the root directory:

OPENAI_API_KEY=your_openai_key

## ▶️ Running the Backend

```bash
python -m main.py
```
👷 Running the Worker

In a separate terminal:
```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES 
rq worker --with-scheduler
```
📡 API Endpoints
POST /chat

Submit user query.

Returns:

{
  "job_id": "xxxx"
}
GET /result/{job_id}

Fetch processed result.

## 🔮 Future Improvements

Streaming responses

Caching layer

Observability (metrics + tracing)

Rate limiting

Frontend UI

Authentication layer

## 💡 Key Learning

GenAI systems are not just about prompting.

They require:

Proper async architecture

Background processing

Queue management

Vector search optimization

Clean separation of concerns
