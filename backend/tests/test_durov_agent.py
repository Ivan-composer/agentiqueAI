"""
Test script for creating and querying multiple Telegram channel agents.
"""
import pytest
from app.services.telegram_service import TelegramService
from app.services.openai_service import generate_embedding
from app.services.pinecone_service import upsert_vectors, query_similar
from app.utils.errors import ServiceUnavailableError
import logging

@pytest.mark.asyncio
async def test_multi_agent_search():
    # Initialize services
    telegram_service = TelegramService()
    
    try:
        # Connect to Telegram
        await telegram_service.connect()
        
        # Process Durov's channel
        durov_channel = "durov"  # Using username directly
        durov_messages = await telegram_service.get_channel_messages(durov_channel, limit=1000)
        logging.info(f"Retrieved {len(durov_messages)} messages from {durov_channel}")
        
        # Process Kyrillic's channel
        kyrillic_channel = "kyrillic"  # Using username directly
        try:
            kyrillic_messages = await telegram_service.get_channel_messages(kyrillic_channel, limit=100)
            logging.info(f"Retrieved {len(kyrillic_messages)} messages from {kyrillic_channel}")
        except Exception as e:
            logging.error(f"Error accessing Kyrillic channel: {e}")
            kyrillic_messages = []
        
        # Process all messages
        vectors = []
        metadata = []
        ids = []
        
        # Process Durov's messages
        for msg in durov_messages:
            if not hasattr(msg, 'message') or not msg.message:
                continue
                
            try:
                embedding = await generate_embedding(msg.message)
                msg_metadata = {
                    'text': msg.message,
                    'date': str(msg.date),
                    'source_link': f"{durov_channel}/{msg.id}",
                    'agent_id': 'durov_test_agent'
                }
                
                vectors.append(embedding)
                metadata.append(msg_metadata)
                ids.append(f"durov_test_agent_{msg.id}")
                
            except Exception as e:
                logging.error(f"Error processing Durov message: {e}")
                continue
        
        # Process Kyrillic's messages
        for msg in kyrillic_messages:
            if not hasattr(msg, 'message') or not msg.message:
                continue
                
            try:
                embedding = await generate_embedding(msg.message)
                msg_metadata = {
                    'text': msg.message,
                    'date': str(msg.date),
                    'source_link': f"{kyrillic_channel}/{msg.id}",
                    'agent_id': 'kyrillic_test_agent'
                }
                
                vectors.append(embedding)
                metadata.append(msg_metadata)
                ids.append(f"kyrillic_test_agent_{msg.id}")
                
            except Exception as e:
                logging.error(f"Error processing Kyrillic message: {e}")
                continue
        
        # Upsert vectors to Pinecone
        if vectors and metadata and ids:
            await upsert_vectors(vectors=vectors, metadata=metadata, ids=ids)
            logging.info(f"Successfully uploaded {len(vectors)} messages to vector database")
        
        # Test search across agents
        query = "what is the best place to live"
        query_embedding = await generate_embedding(query)
        
        # Get similar messages from both agents
        results = await query_similar(query_embedding, top_k=5)
        
        # Build context from results
        if results and 'matches' in results and results['matches']:
            for match in results['matches']:
                agent = match['metadata'].get('agent_id', 'unknown')
                text = match['metadata'].get('text', '')
                score = match['score']
                source = match['metadata'].get('source_link', '')
                logging.info(f"\nAgent: {agent}\nSource: {source}\nScore: {score}\nText: {text}\n{'-'*50}")
                
                # Log relevant insights about living preferences
                if any(word in text.lower() for word in ['city', 'live', 'place', 'country', 'move']):
                    logging.info(f"Found relevant insight about living preferences from {agent}")
        else:
            logging.warning("No relevant context found in the messages.")
        
    except ServiceUnavailableError as e:
        logging.error(f"Service unavailable: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        # Cleanup
        logging.info("Disconnecting from Telegram")
        await telegram_service.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_multi_agent_search()) 