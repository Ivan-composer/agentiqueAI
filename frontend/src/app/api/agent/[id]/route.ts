import { NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    const { id } = params;
    logger.info('Proxying agent deletion request to backend', { id });

    const response = await fetch(`${BACKEND_URL}/agent/${id}`, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
      },
    });

    const data = await response.json();
    logger.info('Received response from backend', { 
      status: response.status,
      data 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to delete agent';
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
    logger.error('Error in agent deletion API route', { error });
    return NextResponse.json(
      { detail: 'Failed to delete agent' },
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
    logger.info('Proxying agent details request to backend', { id });

    const response = await fetch(`${BACKEND_URL}/agent/${id}`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    const data = await response.json();
    logger.info('Received response from backend', { 
      status: response.status,
      data 
    });

    if (!response.ok) {
      const errorDetail = data.detail || 'Failed to fetch agent details';
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
    logger.error('Error in agent details API route', { error });
    return NextResponse.json(
      { detail: 'Failed to fetch agent details' },
      { status: 500 }
    );
  }
} 