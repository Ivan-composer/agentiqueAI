'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { createAgent } from '@/lib/api';
import { Loader2, ArrowLeft } from 'lucide-react';

export default function CreateAgentPage() {
  const router = useRouter();
  const [channelLink, setChannelLink] = useState('');
  const [expertName, setExpertName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const validateChannelLink = (link: string) => {
    const telegramRegex = /^https:\/\/t\.me\/[a-zA-Z0-9_]{5,}$/;
    return telegramRegex.test(link);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validate channel link
    if (!validateChannelLink(channelLink)) {
      setError('Please enter a valid Telegram channel link (e.g., https://t.me/channelname)');
      return;
    }

    // Validate expert name
    if (expertName.length < 2) {
      setError('Expert name must be at least 2 characters long');
      return;
    }

    setIsLoading(true);

    try {
      const agent = await createAgent(channelLink, expertName);
      setSuccess(true);
      // Wait for 1 second to show success message before redirecting
      setTimeout(() => {
        router.push(`/chat/${agent.id}`);
      }, 1000);
    } catch (err: any) {
      setError(err.message || 'Failed to create agent. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-white via-[#E5F7FF]/20 to-white px-4 py-12">
      <div className="w-full max-w-md">
        <div className="flex items-center mb-8">
          <Link 
            href="/"
            className="flex items-center text-gray-600 hover:text-gray-900 transition-colors mr-4"
          >
            <ArrowLeft className="w-5 h-5 mr-1" />
            Back
          </Link>
          <h1 className="text-3xl font-bold text-center flex-1 bg-gradient-to-r from-[#08C6C9] to-[#0098EA] bg-clip-text text-transparent">
            Create AI Agent
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md">
          <div>
            <label htmlFor="channelLink" className="block text-sm font-medium text-gray-700 mb-1">
              Telegram Channel Link
            </label>
            <input
              id="channelLink"
              type="url"
              required
              placeholder="https://t.me/yourchannel"
              value={channelLink}
              onChange={(e) => {
                setChannelLink(e.target.value);
                setError(null);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0098EA] focus:border-transparent"
              disabled={isLoading}
            />
            <p className="mt-1 text-sm text-gray-500">
              Must be a valid Telegram channel link (e.g., https://t.me/channelname)
            </p>
          </div>

          <div>
            <label htmlFor="expertName" className="block text-sm font-medium text-gray-700 mb-1">
              Expert Name
            </label>
            <input
              id="expertName"
              type="text"
              required
              placeholder="John Doe"
              value={expertName}
              onChange={(e) => {
                setExpertName(e.target.value);
                setError(null);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0098EA] focus:border-transparent"
              disabled={isLoading}
            />
            <p className="mt-1 text-sm text-gray-500">
              The name of the expert whose content will be used to create the AI agent
            </p>
          </div>

          {error && (
            <div className="text-red-500 text-sm p-3 bg-red-50 rounded-md border border-red-100">
              {error}
            </div>
          )}

          {success && (
            <div className="text-green-500 text-sm p-3 bg-green-50 rounded-md border border-green-100">
              Agent created successfully! Redirecting to chat...
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white py-2 px-4 rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Creating Agent...
              </>
            ) : (
              'Create Agent'
            )}
          </button>
        </form>
      </div>
    </main>
  );
} 