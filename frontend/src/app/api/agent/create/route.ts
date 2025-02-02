import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';
const DEFAULT_PROMPT_TEMPLATE = `You are an AI expert based on the content from the Telegram channel. You have access to messages and content shared in the channel. When answering questions, use this knowledge to provide accurate and helpful responses. If you're not sure about something, say so rather than making assumptions.

Base your responses on the actual content from the channel, and when relevant, reference specific posts or discussions. Your goal is to help users understand and benefit from the channel's content.

Remember:
1. Only use information from the channel
2. Be clear when you're referencing specific content
3. Maintain the channel owner's tone and style
4. If asked about something not covered in the channel, say so

Current conversation:
{chat_history}

User question: {question}

Please provide a helpful response based on the channel's content:`;

// Helper function to convert base64 to file
function base64ToFile(base64String: string, filename: string = 'profile.jpg'): File {
  // Remove data URL prefix if present
  const base64WithoutPrefix = base64String.replace(/^data:image\/\w+;base64,/, '');
  
  // Convert base64 to binary
  const byteString = Buffer.from(base64WithoutPrefix, 'base64').toString('binary');
  
  // Create an array buffer from the binary string
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }
  
  // Create a blob from the array buffer
  const blob = new Blob([ab], { type: 'image/jpeg' });
  
  // Create a File from the blob
  return new File([blob], filename, { type: 'image/jpeg' });
}

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const channelLink = formData.get('channel_link');
    const userId = formData.get('user_id');
    
    if (!channelLink || !userId) {
      return NextResponse.json(
        { error: 'Missing required fields: channel_link and user_id' },
        { status: 400 }
      );
    }
    
    logger.info('Creating agent...', { channelLink, userId });

    // First, fetch channel info from backend
    const channelInfoResponse = await fetch(`${BACKEND_URL}/telegram/channel-info?channel_link=${encodeURIComponent(channelLink.toString())}`);
    
    if (!channelInfoResponse.ok) {
      const error = await channelInfoResponse.json();
      logger.error('Failed to fetch channel info', { error });
      return NextResponse.json(error, { status: channelInfoResponse.status });
    }
    
    const channelInfo = await channelInfoResponse.json();
    
    // Create form data for backend
    const backendFormData = new FormData();
    backendFormData.append('channel_link', channelLink.toString());
    backendFormData.append('prompt_template', DEFAULT_PROMPT_TEMPLATE);
    backendFormData.append('owner_id', userId.toString());
    
    // Add channel info
    if (channelInfo.profile_photo) {
      // Convert base64 to File object
      const photoFile = base64ToFile(channelInfo.profile_photo);
      backendFormData.append('profile_photo', photoFile);
    }
    if (channelInfo.title) {
      backendFormData.append('channel_title', channelInfo.title);
    }
    if (channelInfo.username) {
      backendFormData.append('channel_username', channelInfo.username);
    }
    if (channelInfo.description) {
      backendFormData.append('channel_description', channelInfo.description);
    }
    if (channelInfo.participants_count) {
      backendFormData.append('channel_participants', channelInfo.participants_count.toString());
    }

    const response = await fetch(`${BACKEND_URL}/agent/create`, {
      method: 'POST',
      body: backendFormData,
    });
    
    const data = await response.json();
    logger.info('Agent creation response:', { 
      status: response.status,
      data 
    });
    
    if (!response.ok) {
      logger.error('Failed to create agent', { 
        status: response.status,
        error: data 
      });
      return NextResponse.json(data, { status: response.status });
    }
    
    return NextResponse.json(data);
    
  } catch (error) {
    logger.error('Error in /api/agent/create', { error });
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
} 