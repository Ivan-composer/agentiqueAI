import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

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

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { channel_link } = body;
    
    if (!channel_link) {
      return NextResponse.json(
        { error: 'Missing required field: channel_link' },
        { status: 400 }
      );
    }
    
    logger.info('Creating test user...', { channel_link });
    
    // First create a test user
    const userResponse = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/auth/telegram/login?telegram_id=test_user&username=test_user`,
      {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      }
    );

    const userResponseData = await userResponse.json();
    logger.info('User creation response:', { 
      status: userResponse.status,
      data: userResponseData 
    });

    if (!userResponse.ok) {
      const errorDetail = userResponseData.detail || 'Failed to create test user';
      logger.error('Failed to create test user', { 
        status: userResponse.status,
        error: errorDetail 
      });
      return NextResponse.json(
        { error: errorDetail },
        { status: userResponse.status }
      );
    }

    const userId = userResponseData.id;
    logger.info('Successfully created test user', { userId });
    
    // Create agent with form data
    logger.info('Creating agent...', { channel_link, userId });
    const formData = new URLSearchParams();
    formData.append('channel_link', channel_link);
    formData.append('prompt_template', DEFAULT_PROMPT_TEMPLATE);
    formData.append('owner_id', userId);

    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/agent/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
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