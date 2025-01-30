-- Rename chat_history table to chat_messages
ALTER TABLE IF EXISTS chat_history RENAME TO chat_messages;

-- Rename indexes
ALTER INDEX IF EXISTS idx_chat_history_user_id RENAME TO idx_chat_messages_user_id;
ALTER INDEX IF EXISTS idx_chat_history_agent_id RENAME TO idx_chat_messages_agent_id;

-- Add sources column if it doesn't exist
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS sources JSONB DEFAULT '[]'::jsonb;

-- Add context column if it doesn't exist
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS context TEXT; 