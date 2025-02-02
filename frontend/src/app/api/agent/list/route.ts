import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function GET() {
  try {
    logger.info('Proxying agent list request to backend');

    const response = await fetch(`${BACKEND_URL}/agent/list`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
      cache: 'no-store', // Disable caching
    });

    const data = await response.json();
    logger.info('Received response from backend', { 
      status: response.status,
      data 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to list agents';
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
    logger.error('Error in agent list API route', { error });
    return NextResponse.json(
      { detail: 'Failed to fetch agents' },
      { status: 500 }
    );
  }
} 