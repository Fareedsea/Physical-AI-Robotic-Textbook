from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI
import os
from rag.retrieval import retrieve_context

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class QueryRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = [] # List of {"role": "user"|"assistant", "content": "..."}

class SelectedTextQueryRequest(BaseModel):
    question: str
    selected_text: str
    history: Optional[List[dict]] = []

def generate_answer(question: str, context: list[str], history: list[dict] = []) -> str:
    """
    Generates an answer using OpenAI ChatCompletion, grounded in the provided context.
    """
    
    system_prompt = """You are an expert AI Robotics Professor for the 'Physical AI Robotics Textbook'.
    Use the provided context to answer the student's question accurately.
    If the answer is not in the context, use your general knowledge but mention that it's outside the course material.
    Keep answers concise, technical, and encouraging.
    """
    
    context_str = "\n\n".join(context)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history (last 4 messages to save tokens)
    messages.extend(history[-4:])
    
    # Add retrieved context and current question
    user_content = f"Context:\n{context_str}\n\nQuestion: {question}"
    messages.append({"role": "user", "content": user_content})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo if cost is a concern
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I'm sorry, I encountered an error while generating the response."

async def process_query(request: QueryRequest):
    # 1. Retrieve relevant documents
    context = retrieve_context(request.question)
    
    # 2. Generate answer
    answer = generate_answer(request.question, context, request.history)
    
    return {
        "answer": answer,
        "sources": context # Return sources for citation/debugging
    }

async def process_selected_query(request: SelectedTextQueryRequest):
    # For selected text, we prioritize the selected content as the primary context
    # We might also fetch related docs if needed, but usually selected text IS the context.
    
    context = [request.selected_text] # High priority context
    
    # Optionally: fetch more related to the question to supplement
    # additional_context = retrieve_context(request.question, limit=1)
    # context.extend(additional_context)
    
    answer = generate_answer(request.question, context, request.history)
    
    return {
        "answer": answer,
        "used_selection": True
    }
