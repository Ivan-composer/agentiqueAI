from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import VectorStore
from . import llm_service, db_service
from .vector_service import vector_service  # Import the singleton instance

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

# Initialize LLM
llm = llm_service.current_llm  # Use the current active LLM

async def process_and_store_text(text: str, agent_id: str) -> bool:
        """
    Process text content and store in vector database
    1. Split text into chunks
    2. Generate embeddings
    3. Store in Pinecone
    """
    try:
        # Split text into chunks
        chunks = text_splitter.split_text(text)
            
        # Generate embeddings for chunks
        embeddings = await llm_service.get_embeddings(chunks)
                
        if not embeddings:
            return False
            
        # Prepare vectors with metadata
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors.append({
                "id": f"{agent_id}-{i}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "agent_id": agent_id
                }
            })
        
        # Store in vector database
        await vector_service._upsert_vectors(vectors)
        return True
        
    except Exception as e:
        print(f"Error processing text: {str(e)}")
        return False
            
async def generate_response(question: str, agent_id: str) -> Dict[str, Any]:
        """
    Generate a response using RAG (Retrieval Augmented Generation)
    1. Get agent details
    2. Retrieve relevant context
    3. Generate response using LLM
    """
    try:
        print(f"\n[RAGService] Starting response generation for question: {question}")
        
        # Get agent details
        agent = await db_service.get_agent(agent_id)
        if not agent:
            print("[RAGService] Agent not found")
            return {"error": "Agent not found"}
            
        print(f"[RAGService] Found agent: {agent.get('name')}")
                
        # Get embeddings for the question
        print("[RAGService] Getting question embedding...")
        question_embedding = await llm_service.get_embeddings([question])
        if not question_embedding:
            print("[RAGService] Failed to generate question embedding")
            return {"error": "Failed to generate question embedding"}
        
        print(f"[RAGService] Got question embedding with dimension: {len(question_embedding[0])}")
        
        # Search for relevant context
        print("[RAGService] Searching for relevant context...")
        results = await vector_service.search_vectors(
            query_vector=question_embedding[0],
            agent_id=agent_id,
            top_k=3
            )
            
        print(f"[RAGService] Found {len(results)} results")
                
        if not results:
            print("[RAGService] No relevant context found")
            return {"error": "No relevant context found"}
                
        # Extract and combine context
        context = "\n\n".join([
            match.metadata.get("text", "")
            for match in results
            if match.metadata
        ])

        print(f"[RAGService] Combined context length: {len(context)}")
        print(f"[RAGService] Context preview: {context[:200]}...")

        # Format prompt with context
        prompt = llm_service.AGENT_PROMPT.format(
            agent_name=agent.get("name", "AI Agent"),
            context=context,
            question=question
            )
            
        print("[RAGService] Generating final response...")
        # Generate response using async function
        response = await llm_service.generate_response(prompt)
        
        print("[RAGService] Successfully generated response")
        return {
            "response": response,
            "context": context,
            "sources": [
                {
                    "text": match.metadata.get("text", ""),
                    "score": match.score
                }
                for match in results
                if match.metadata
            ]
        }
        
    except Exception as e:
        print(f"\n[RAGService] Error generating response:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

async def generate_rag_response(query: str, agent_id: str = None) -> Dict[str, Any]:
    """
    Generate a response using RAG:
    1. Generate query embedding
    2. Search similar vectors
    3. Generate response with context
    """
    try:
        # Get query embedding
        query_embedding = await llm_service.get_query_embedding(query)
        if not query_embedding:
            return {"error": "Failed to generate query embedding"}
        
        # Search similar vectors
        similar_chunks = await vector_service.search_vectors(query_embedding, agent_id)
        if not similar_chunks:
            return {"error": "No relevant information found"}
        
        # Prepare context from similar chunks
        context = "\n\n".join([chunk.metadata["text"] for chunk in similar_chunks])
        
        # Generate response with context
        prompt = f"""Based on the following context, answer the question. 
        If you cannot answer based on the context alone, say so.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:"""
        
        response = await llm_service.generate_response(prompt)
        
            return {
            "response": response,
            "sources": [{"text": chunk.metadata["text"]} for chunk in similar_chunks]
            }

    except Exception as e:
        print(f"Error generating RAG response: {e}")
        return {"error": "Failed to generate response"} 