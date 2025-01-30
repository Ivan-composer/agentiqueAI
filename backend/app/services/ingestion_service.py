from typing import Optional, List, Dict, Any
from . import db_service, rag_service
from .telegram_service import telegram_service
from app.models.agent import Agent
from .vector_service import VectorService

class IngestionService:
    def __init__(self):
        self.vector_service = VectorService()

    async def ingest_channel(self, channel_link: str, agent: Agent) -> bool:
        """
        Full ingestion pipeline:
        1. Validate channel
        2. Fetch messages
        3. Process and store vectors
        4. Update agent status
        """
        try:
            print(f"\n[IngestionService] Starting ingestion for channel: {channel_link}")
            
            # Step 1: Validate channel
            print("[IngestionService] Validating channel...")
            is_valid = await telegram_service.validate_channel(channel_link)
            if not is_valid:
                print("[IngestionService] Channel validation failed!")
                await db_service.update_agent_status(agent.id, "failed")
                return False
            print("[IngestionService] Channel validation successful!")
            
            # Step 2: Fetch messages
            print("[IngestionService] Fetching messages...")
            messages = await telegram_service.fetch_channel_messages(channel_link)
            print(f"[IngestionService] Fetched {len(messages) if messages else 0} messages")
            
            if not messages:
                print("[IngestionService] No messages fetched!")
                await db_service.update_agent_status(agent.id, "failed")
                return False
            
            # Print first message for debugging
            if messages:
                print("\n[IngestionService] First message preview:")
                print(f"Message ID: {messages[0].get('message_id', 'unknown')}")
                print(f"Text: {messages[0].get('text', '')[:100]}...")
            
            # Step 3: Process and store vectors
            print("\n[IngestionService] Processing and storing vectors...")
            success = await self.vector_service.process_and_store(messages, agent.id)
            if not success:
                print("[IngestionService] Vector processing failed!")
                await db_service.update_agent_status(agent.id, "failed")
                return False
            
            # Check vector count
            vector_count = await self.vector_service.count_vectors(agent.id)
            print(f"[IngestionService] Stored {vector_count} vectors")
            
            if vector_count == 0:
                print("[IngestionService] No vectors were stored!")
                await db_service.update_agent_status(agent.id, "failed")
                return False
            
            # Update agent status to ready
            print("[IngestionService] Ingestion completed successfully")
            await db_service.update_agent_status(agent.id, "ready")
            return True
            
        except Exception as e:
            print(f"\n[IngestionService] Error during ingestion:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            import traceback
            traceback.print_exc()
            await db_service.update_agent_status(agent.id, "failed")
            return False

    async def reingest_channel(self, agent_id: str, channel_link: str) -> bool:
        """
        Re-ingest a channel's content:
        1. Delete existing vectors
        2. Run full ingestion again
        """
        try:
            # Update status to reingesting
            await db_service.update_agent_status(agent_id, "reingesting")
            
            # Delete existing vectors
            await self.vector_service.delete_agent_vectors(agent_id)
            
            # Get agent details
            agent_data = await db_service.get_agent(agent_id)
            if not agent_data:
                print("[IngestionService] Agent not found!")
                return False
            
            agent = Agent(**agent_data)
            
            # Run ingestion
            return await self.ingest_channel(channel_link, agent)
            
        except Exception as e:
            print(f"Error during reingestion: {e}")
            await db_service.update_agent_status(agent_id, "failed")
            return False

# Create a singleton instance
ingestion_service = IngestionService() 