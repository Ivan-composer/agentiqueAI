import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

// Test user UUID - TODO: Replace with real user ID from auth
const TEST_USER_ID = '11111111-1111-1111-1111-111111111111';

export async function POST(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    const body = await request.json();
    const { message } = body;

    logger.info('Proxying chat message to backend', { id, message });

    // Create form data
    const formData = new FormData();
    formData.append('message', message);
    formData.append('user_id', TEST_USER_ID);

    const response = await fetch(`${BACKEND_URL}/agent/${id}/chat`, {
      method: 'POST',
      body: formData,
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