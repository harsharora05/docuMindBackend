from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
load_dotenv()


client = OpenAI()
embeddings=OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_store = QdrantVectorStore.from_existing_collection(
   embedding=embeddings,
   collection_name="first_rag",
   url="http://localhost:6333",
)



def process_query(query:str):
    print("searching for relevant chunks")
    similarity_result = vector_store.similarity_search(query=query)

    context = "\n\n\n".join([f" page_number:{res.metadata['page']}\npage_content:{res.page_content}\nmeta_data: {res.metadata}"  for res in similarity_result])
    SYSTEM_PROMPT = f'''
    You are an AI assistant. Answer the user’s question strictly using the provided context. Include the page number(s) from where the answer was found. If the answer is not in the context, say "Answer not found in the provided context." Do not add any external information.
    CONTEXT:{context}
    '''

    response=client.chat.completions.create(
        model='gpt-5-mini',
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":query}
        ]
    )
    return response.choices[0].message.content



