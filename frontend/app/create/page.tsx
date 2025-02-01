'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { createAgent } from '@/lib/api';

export default function CreateAgentPage() {
  const router = useRouter();
  const [channelLink, setChannelLink] = useState('');
  const [expertName, setExpertName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const agent = await createAgent(channelLink, expertName);
      router.push(`/chat/${agent.id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col items-center bg-gradient-to-b from-white via-[#E5F7FF]/20 to-white px-4 py-12">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-[#08C6C9] to-[#0098EA] bg-clip-text text-transparent">
          Create AI Agent
        </h1>

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
              onChange={(e) => setChannelLink(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0098EA] focus:border-transparent"
            />
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
              onChange={(e) => setExpertName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0098EA] focus:border-transparent"
            />
          </div>

          {error && (
            <div className="text-red-500 text-sm p-3 bg-red-50 rounded-md">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white py-2 px-4 rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Creating...' : 'Create Agent'}
          </button>
        </form>
      </div>
    </main>
  );
} 