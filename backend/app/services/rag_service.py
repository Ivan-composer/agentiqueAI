"""
RAG service for retrieving and generating responses using Pinecone and OpenAI.

This module provides a unified approach to RAG (Retrieval Augmented Generation)
for both chat and search functionalities. It uses the same core logic but
allows filtering by agent_id for chat-specific queries.
"""
from typing import Optional, List, Dict, Any
from app.services.openai_service import generate_embedding, generate_completion
from app.services.pinecone_service import query_similar
from app.utils.logger import logger

# Number of chunks to retrieve from Pinecone
TOP_K = 10

def format_references(chunks: List[Dict[str, Any]]) -> str:
    """
    Format retrieved chunks into a bullet-point list with source references.
    
    Args:
        chunks: List of chunks with text and metadata
        
    Returns:
        Formatted string with bullet points and source links
    """
    references = []
    for chunk in chunks:
        text = chunk['text']
        source = chunk['metadata'].get('source_link', 'Unknown source')
        score = chunk.get('score', 0.0)
        references.append(f"• {text} (source: {source}, relevance: {score:.3f})")
        # Log each chunk for debugging
        logger.debug("Retrieved chunk: %s (score: %.3f)", text[:100] + "...", score)
    return "\n".join(references)

async def rag_retrieve_and_summarize(
    query: str,
    agent_id: Optional[str] = None,
    mode: str = "chat"
) -> str:
    """
    Perform RAG: embed query, retrieve from Pinecone, generate completion.
    
    Args:
        query: The user's query
        agent_id: Optional agent ID to filter results
        mode: Either "chat" or "search"
        
    Returns:
        Generated response with references
    """
    try:
        # Generate query embedding
        query_embedding = await generate_embedding(query)
        if not query_embedding:
            logger.error("Failed to generate embedding for query: %s", query)
            return "Failed to process your query. Please try again."
            
        # Query Pinecone
        filter_params = {"agent_id": agent_id} if agent_id else {}
        logger.debug("Querying Pinecone with filter: %s", filter_params)
        chunks = await query_similar(
            query_embedding,
            top_k=TOP_K,
            filter_params=filter_params
        )
        
        if not chunks:
            logger.warning("No chunks found for query '%s' with filter %s", query, filter_params)
            return "I couldn't find any relevant information to answer your question."
            
        # Log number of chunks retrieved
        logger.info("Retrieved %d chunks for query '%s'", len(chunks), query)
        
        # Format context
        context = format_references(chunks)
        
        # Build prompt
        if mode == "chat":
            prompt = f"""You are an AI expert based on the content from a specific channel. 
Answer the following question using ONLY the information provided in the context below.
If you can't find a relevant answer in the context, say so.
Always reference your sources.

Context:
{context}

Question: {query}

Please provide a helpful response based on the context:"""
        else:  # search mode
            prompt = f"""You are a search assistant. Summarize the most relevant information from the context below
to answer the user's query. Include all relevant source links.

Context:
{context}

Query: {query}

Please provide a summary of the relevant information:"""
            
        # Generate completion
        response = await generate_completion(prompt)
        return response
        
    except Exception as e:
        logger.error("Error in RAG process: %s", str(e))
        return "I encountered an error while processing your request. Please try again." 