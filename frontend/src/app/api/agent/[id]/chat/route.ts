import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    
    // Parse form data from request
    const formData = await request.formData();
    const message = formData.get('message');
    const userId = formData.get('user_id');
    
    if (!message || !userId) {
      logger.error('Missing required fields', { message, userId });
      return NextResponse.json(
        { detail: 'Message and user_id are required' },
        { status: 400 }
      );
    }

    logger.info('Proxying chat message to backend', { 
      id, 
      userId,
      messageLength: message.toString().length 
    });

    // Create form data for backend
    const backendFormData = new FormData();
    backendFormData.append('message', message.toString());
    backendFormData.append('user_id', userId.toString());

    // Convert FormData to URLSearchParams for proper sending
    const searchParams = new URLSearchParams();
    searchParams.append('message', message.toString());
    searchParams.append('user_id', userId.toString());

    const response = await fetch(`${BACKEND_URL}/agent/${id}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: searchParams,
    });

    const data = await response.json();
    logger.info('Received response from backend', { 
      status: response.status,
      data 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to send message';
      logger.error('Backend returned error', { 
        status: response.status,
        error: errorDetail 
      });
      return NextResponse.json(
        { detail: errorDetail },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    logger.error('Error in chat API route', { error });
    return NextResponse.json(
      { detail: 'Failed to process chat message' },
      { status: 500 }
    );
  }
}

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('user_id');
    
    if (!userId) {
      logger.error('Missing user_id parameter');
      return NextResponse.json(
        { detail: 'user_id parameter is required' },
        { status: 400 }
      );
    }

    logger.info('Fetching chat history from backend', { id, userId });

    const response = await fetch(
      `${BACKEND_URL}/agent/${id}/chat_history?user_id=${userId}`,
      { method: 'GET' }
    );

    const data = await response.json();
    logger.info('Received chat history from backend', { 
      status: response.status,
      messageCount: data.messages?.length 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to fetch chat history';
      logger.error('Backend returned error', { 
        status: response.status,
        error: errorDetail 
      });
      return NextResponse.json(
        { detail: errorDetail },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    logger.error('Error in chat history API route', { error });
    return NextResponse.json(
      { detail: 'Failed to fetch chat history' },
      { status: 500 }
    );
  }
} 