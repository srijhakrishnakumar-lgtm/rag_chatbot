from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import EmailStr, BaseModel
import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq

app = FastAPI()
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)
employees = {}
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("documents_new")

class Employee(BaseModel):
    employee_id: int
    name: str
    age: int
    department: str
    email: EmailStr
    salary: float

@app.get("/welcome")
def welcome_func():
    return {"message": "Hello World!"}

# @app.post("/chat")
# def user_chat(msg: str):
#     if msg.lower() == "hi":
#         message = "Hello!"
#     else:
#         message = "Welcome"
#     return {"message": message}

@app.post("/employee-details-insert")
def employee_details_insertion(
    employee: Employee
):
    if employee.employee_id in employees:
        return {"message": "Employee id is already exist"}
    employees[employee.employee_id]={
            "name": employee.name,
            "age": employee.age,
            "department": employee.department,
            "email": employee.email,
            "salary": employee.salary
    }
    return {"message": "Added Successfully"}


@app.post("/data-insertion")
async def file_uploading(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    pdf = fitz.open(f"uploads/{file.filename}")

    text = ""

    for page in pdf:
        text += page.get_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
        )   
    
    chunks = splitter.split_text(text)
    embeddings = model.encode(chunks)
    # embedding_data = []

    # for index, (chunk, embedding) in enumerate(zip(chunks, embeddings), start=1):
    #     embedding_data.append({
    #         "chunk_id": index,
    #         "chunk": chunk,
    #         "embedding_dimension": len(embedding),
    #         "embedding": embedding.tolist()   # Convert NumPy array to list
    #     })
    collection.add(
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=[e.tolist() for e in embeddings],
        metadatas=[
            {"source": file.filename, "chunk_id": i}
            for i in range(len(chunks))
        ],
    )
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "number_of_pages": len(pdf),
        "extracted_text": text,
        "length_of_text": len(text),
        "chunks": chunks,
        "number_of_chunks": len(chunks),
        # "embedded_data": embedding_data,
        "message": "Uploaded Successfully"
    }


@app.get("/download/{filename}")
async def download_file(filename: str):

    file_path = os.path.join("uploads", filename)

    # Check whether file exists
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )

@app.get("/data-inserted")
async def inserted_data():
    results = collection.get(
        include=["documents", "metadatas"]
    )
    print(collection.get(
        include=["documents", "metadatas","embeddings"]
    )) 
    # results = collection.count()
    return {"results": results}

@app.post("/chat")
def chat(question: str):
    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents"]
    )
    print(results)
    context = "\n\n".join(results["documents"][0])
    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            },
        ],
    )
    answer = response.choices[0].message.content
    return {
        "question": question,
        "retrieved_context": context,
        "answer": answer
    }