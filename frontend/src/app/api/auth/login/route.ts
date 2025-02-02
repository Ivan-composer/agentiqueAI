import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function POST(request: Request) {
  try {
    const formData = await request.formData();
    const telegramId = formData.get('telegram_id');
    const username = formData.get('username');
    
    if (!telegramId || !username) {
      return NextResponse.json(
        { error: 'Missing required fields: telegram_id and username' },
        { status: 400 }
      );
    }
    
    logger.info('Creating temporary user...', { telegramId, username });

    // Build query string for the login endpoint
    const queryString = new URLSearchParams({
      telegram_id: telegramId.toString(),
      username: username.toString()
    }).toString();

    const response = await fetch(`${BACKEND_URL}/auth/telegram/login?${queryString}`, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      }
    });
    
    const data = await response.json();
    logger.info('User creation response:', { 
      status: response.status,
      data 
    });
    
    if (!response.ok) {
      logger.error('Failed to create user', { 
        status: response.status,
        error: data 
      });
      return NextResponse.json(
        { error: data.detail || 'Failed to create user' },
        { status: response.status }
      );
    }
    
    return NextResponse.json(data);
    
  } catch (error) {
    logger.error('Error in /api/auth/login', { error });
    return NextResponse.json(
      { error: 'Internal server error', details: error instanceof Error ? error.message : String(error) },
      { status: 500 }
    );
  }
} 