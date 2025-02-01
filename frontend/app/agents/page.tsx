'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, MessageSquare, Loader2, Plus } from 'lucide-react';
import { getAgents } from '@/lib/api';
import type { Agent } from '@/lib/api';

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const agentList = await getAgents();
        setAgents(agentList);
      } catch (err: any) {
        setError(err.message || 'Failed to load agents. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchAgents();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-b from-white via-[#E5F7FF]/20 to-white">
      {/* Header */}
      <div className="flex items-center p-4 border-b bg-white/80 backdrop-blur-sm">
        <Link
          href="/"
          className="flex items-center text-gray-600 hover:text-gray-900 transition-colors"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back to Home
        </Link>
        <h1 className="text-xl font-semibold text-center flex-1 bg-gradient-to-r from-[#08C6C9] to-[#0098EA] bg-clip-text text-transparent">
          AI Agents
        </h1>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto p-4">
        {/* Create New Agent Button */}
        <Link
          href="/create"
          className="mb-8 inline-flex items-center bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white px-6 py-3 rounded-md hover:opacity-90 transition-opacity"
        >
          <Plus className="w-5 h-5 mr-2" />
          Create New Agent
        </Link>

        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center text-gray-500 py-12">
            <Loader2 className="w-6 h-6 animate-spin mr-2" />
            Loading agents...
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-red-500 text-sm p-3 bg-red-50 rounded-md border border-red-100 mb-4">
            {error}
          </div>
        )}

        {/* No Agents State */}
        {!isLoading && !error && agents.length === 0 && (
          <div className="text-center text-gray-500 py-12">
            <p className="mb-4">No AI agents found</p>
            <p className="text-sm">
              Create your first agent to start chatting!
            </p>
          </div>
        )}

        {/* Agents Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
            >
              <h2 className="text-lg font-semibold text-gray-900 mb-2">
                {agent.expert_name}
              </h2>
              <p className="text-gray-600 text-sm mb-4 truncate">
                {agent.channel_link}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">
                  Created: {new Date(agent.created_at).toLocaleDateString()}
                </span>
                <Link
                  href={`/chat/${agent.id}`}
                  className="inline-flex items-center text-[#0098EA] hover:underline"
                >
                  <MessageSquare className="w-4 h-4 mr-1" />
                  Chat
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
} 