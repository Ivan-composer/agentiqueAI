"""
rag_service.py: Unifies retrieval for chat vs. search.

This module provides a unified approach to RAG (Retrieval Augmented Generation)
for both chat and search functionalities. It uses the same core logic but
allows filtering by agent_id for chat-specific queries.
"""
from typing import Optional, List, Dict, Any
from app.services.openai_service import generate_embedding, generate_completion
from app.services.pinecone_service import index, query_similar

# Number of chunks to retrieve from Pinecone
TOP_K = 5

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
        references.append(f"• {text} (source: {source})")
    return "\n".join(references)

async def rag_retrieve_and_summarize(
    query: str,
    agent_id: Optional[str] = None,
    mode: str = "chat"
) -> str:
    """
    Unified RAG function that handles both chat and search queries.

    Args:
        query: The user's query text
        agent_id: Optional agent ID to filter results (used in chat mode)
        mode: Either "chat" or "search" to determine response style

    Returns:
        Generated response with references

    Raises:
        ValueError: If mode is invalid
    """
    if mode not in ["chat", "search"]:
        raise ValueError("Invalid mode. Must be 'chat' or 'search'")

    # Generate query embedding
    query_embedding = await generate_embedding(query)

    # Prepare filter for Pinecone query
    filter_dict = {"agent_id": agent_id} if agent_id else {}

    # Query Pinecone
    results = await query_similar(
        query_vector=query_embedding,
        top_k=TOP_K,
        agent_id=agent_id if mode == "chat" else None
    )

    # Extract chunks and format references
    chunks = [
        {
            'text': match['metadata'].get('text', ''),
            'metadata': match['metadata']
        }
        for match in results
    ]

    # Format references
    references = format_references(chunks)

    # Build prompt based on mode
    if mode == "chat":
        prompt = f"Based on the following context, answer the user's question: {query}\n\nContext:\n{references}"
    else:  # search mode
        prompt = f"Summarize the following search results for the query: {query}\n\nResults:\n{references}"

    # Generate completion
    return await generate_completion(prompt) 