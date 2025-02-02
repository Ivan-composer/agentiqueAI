import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { telegram_id, username } = body;

    logger.info('Proxying Telegram login request to backend', { 
      telegram_id,
      username,
      backendUrl: BACKEND_URL 
    });

    const response = await fetch(
      `${BACKEND_URL}/auth/telegram/login?telegram_id=${encodeURIComponent(telegram_id)}&username=${encodeURIComponent(username)}`,
      {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
        },
      }
    );

    const data = await response.json();
    logger.info('Received response from backend', { 
      status: response.status,
      data 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to login';
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
    logger.error('Error in Telegram login API route', { error });
    return NextResponse.json(
      { detail: 'Failed to process login request' },
      { status: 500 }
    );
  }
} 