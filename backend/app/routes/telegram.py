from fastapi import APIRouter, HTTPException
from app.services.telegram_service import TelegramService
from app.utils.logger import logger
from app.utils.errors import TelegramError
from app.models.db_models import ChannelInfo
import traceback

router = APIRouter()

@router.get("/channel-info")
async def get_channel_info(channel_link: str) -> ChannelInfo:
    """
    Get information about a Telegram channel including profile photo.
    Returns a ChannelInfo model with the profile photo encoded in base64.
    """
    logger.info(f"Received request for channel info: {channel_link}")
    
    try:
        logger.info("Initializing TelegramService...")
        async with TelegramService() as telegram:
            logger.info("TelegramService initialized successfully")
            try:
                channel_info = await telegram.get_channel_info(channel_link)
                logger.info(f"Successfully retrieved channel info for {channel_link}")
                return ChannelInfo(**channel_info)
            except Exception as e:
                logger.error(f"Error in get_channel_info: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
    except TelegramError as e:
        logger.error(f"Telegram error for channel {channel_link}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error(f"Unexpected error for channel {channel_link}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) 