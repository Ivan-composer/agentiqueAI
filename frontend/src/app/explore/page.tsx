"use client";

import { useState, useEffect } from 'react';
import { PlusCircle, Loader2, MessageCircle, Trash2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LoadingDots } from '@/components/ui/loading-dots';
import { logger } from '@/lib/logger';
import Link from 'next/link';

interface CreateAgentResponse {
  agent_id: string;
  message_count: number;
  vector_count: number;
  status: 'success' | 'created_without_messages' | 'error';
}

interface ErrorResponse {
  detail: string;
}

interface Agent {
  id: string;
  expert_name: string;
  status: string;
  created_at: string;
}

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

/**
 * Explore page component showing available AI agents and creation option.
 * Integrates with backend /agent/create endpoint.
 */
export default function ExplorePage() {
  const [isCreating, setIsCreating] = useState(false);
  const [telegramLink, setTelegramLink] = useState('');
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [isLoadingAgents, setIsLoadingAgents] = useState(true);

  // Fetch agents on mount
  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const response = await fetch('/api/agent/list');
        const data = await response.json();
        if (response.ok && data.agents) {
          setAgents(data.agents);
        }
      } catch (error) {
        console.error('Error fetching agents:', error);
      } finally {
        setIsLoadingAgents(false);
      }
    };

    fetchAgents();
  }, []);

  const handleCreateAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setProgress(0);
    
    if (!telegramLink) {
      setError('Please enter a Telegram channel link');
      return;
    }
    
    // Get user ID from local storage
    const userId = localStorage.getItem('userId');
    if (!userId) {
      setError('Please log in to create an agent');
      return;
    }
    
    setIsCreating(true);
    
    try {
      // Start progress animation
      setProgress(10);
      
      // Create form data
      const formData = new FormData();
      formData.append('channel_link', telegramLink);
      formData.append('user_id', userId);
      
      // Call backend API to create agent
      const response = await fetch('/api/agent/create', {
        method: 'POST',
        body: formData,
      });
      
      // Update progress
      setProgress(50);
      
      if (!response.ok) {
        throw new Error(await response.text());
      }
      
      const data = await response.json();
      
      // Final progress
      setProgress(100);
      
      setSuccess('Agent created successfully!');
      
      // Reset form
      setTelegramLink('');
      
      // Refresh the agents list
      refreshAgents();
      
    } catch (error) {
      logger.error('Error creating agent', { error });
      
      // Extract error message
      let errorMessage = 'Failed to create agent';
      
      if (error instanceof Error) {
        errorMessage = error.message;
      } else if (typeof error === 'string') {
        errorMessage = error;
      } else if (error && typeof error === 'object') {
        errorMessage = JSON.stringify(error);
      }

      // Show a more helpful message based on the error
      if (errorMessage.includes('backend server')) {
        setError('Could not connect to the server. Please ensure the backend is running and try again.');
      } else if (errorMessage.includes('timed out')) {
        setError('The request took too long. The server might be busy processing a large channel. Please try again.');
      } else if (errorMessage.includes('Invalid request format')) {
        setError('There was a problem with the request format. Please check your input and try again.');
      } else if (errorMessage.includes('Failed to fetch')) {
        setError('Could not connect to the server. Please check your internet connection and try again.');
      } else if (errorMessage.includes('channel_access')) {
        setError('Could not access the channel. Please make sure:\n' +
          '• The channel exists and is public\n' +
          '• You entered the correct channel link/username\n' +
          '• You have permission to access the channel');
      } else {
        setError(`Error: ${errorMessage}`);
      }
    } finally {
      setIsCreating(false);
      setProgress(0);
    }
  };

  // After successful agent creation, refresh the agents list
  const refreshAgents = async () => {
    try {
      const response = await fetch('/api/agent/list');
      const data = await response.json();
      if (response.ok && data.agents) {
        setAgents(data.agents);
      }
    } catch (error) {
      console.error('Error refreshing agents:', error);
    }
  };

  const handleDeleteAgent = async (agentId: string) => {
    try {
      const response = await fetch(`/api/agent/${agentId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to delete agent');
      }

      // Refresh the agents list after successful deletion
      refreshAgents();
    } catch (error) {
      console.error('Error deleting agent:', error);
      setError(error instanceof Error ? error.message : 'Failed to delete agent');
    }
  };

  return (
    <div className="space-y-8 pb-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-2xl font-bold mb-2">Explore AI Agents</h1>
        <p className="text-muted-foreground">Create or discover AI agents</p>
      </div>

      {/* Create Agent Section */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50">
        <CardHeader>
          <CardTitle>Create New AI Agent</CardTitle>
          <CardDescription>Enter a Telegram channel link to create an AI agent</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleCreateAgent} className="space-y-4">
            <div className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="telegram-link" className="text-sm text-muted-foreground">
                  Telegram Channel Link
                </label>
                <Input
                  id="telegram-link"
                  type="text"
                  value={telegramLink}
                  onChange={(e) => setTelegramLink(e.target.value)}
                  placeholder="Enter Telegram channel link or username"
                  disabled={isCreating}
                />
                <p className="text-xs text-muted-foreground">
                  Examples:<br />
                  • Full link: https://t.me/channelname<br />
                  • Just username: channelname
                </p>
              </div>
            </div>
            
            {isCreating && progress > 0 && (
              <div className="space-y-2">
                <div className="h-2 bg-muted rounded-full overflow-hidden">
                  <div 
                    className="h-full bg-primary transition-all duration-500 ease-out"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-sm text-muted-foreground text-center">
                  Processing channel... {progress}%
                </p>
              </div>
            )}

            {error && (
              <div className="text-sm text-red-500 text-center p-3 bg-red-50 rounded-md">
                {error}
              </div>
            )}

            {success && (
              <div className="text-sm text-green-500 text-center p-3 bg-green-50 rounded-md">
                {success}
              </div>
            )}

            <Button
              type="submit"
              className="w-full"
              disabled={isCreating}
            >
              {isCreating ? 'Creating...' : 'Create Agent'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Agent List */}
      <Card>
        <CardHeader>
          <CardTitle>Available Agents</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoadingAgents ? (
            <div className="text-center py-8">
              <LoadingDots className="text-primary mx-auto mb-4" />
              <p className="text-muted-foreground">
                Loading available agents...
              </p>
            </div>
          ) : agents.length > 0 ? (
            <div className="space-y-4">
              {agents.map((agent) => (
                <Card key={agent.id}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-lg">{agent.expert_name}</CardTitle>
                        <CardDescription className="mt-1">
                          Created {new Date(agent.created_at).toLocaleDateString()}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="flex justify-between items-center">
                      <div className="text-sm text-muted-foreground">
                        Status: {agent.status}
                      </div>
                      <div className="flex gap-2">
                        {agent.expert_name !== 'TateB' && (
                          <Button
                            variant="destructive"
                            size="icon"
                            onClick={() => handleDeleteAgent(agent.id)}
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        )}
                        <Link href={`/agent/${agent.id}`}>
                          <Button>
                            <MessageCircle className="w-4 h-4 mr-2" />
                            Start Chat
                          </Button>
                        </Link>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <div className="text-center text-muted-foreground py-8">
              No agents available yet. Create one to get started!
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
} 