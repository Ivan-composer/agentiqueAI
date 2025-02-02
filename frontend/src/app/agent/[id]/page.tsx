"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Send, User2 } from 'lucide-react';
import Link from 'next/link';
import Image from 'next/image';
import { useChatStore, type Message, sendMessage } from '@/lib/chat-service';
import { LoadingDots } from '@/components/ui/loading-dots';
import { logger } from '@/lib/logger';

interface Agent {
  id: string;
  expert_name: string;
  status: string;
  created_at: string;
  profile_photo_url?: string;
}

/**
 * Agent Chat page for interacting with a specific AI agent.
 */
export default function AgentChatPage() {
  const params = useParams();
  const id = Array.isArray(params.id) ? params.id[0] : params.id;
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { messages: allMessages, addMessage, setMessages } = useChatStore();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [isLoadingAgent, setIsLoadingAgent] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  // Get current agent's messages
  const currentMessages = id ? (allMessages[id] || []) : [];

  // Fetch agent details
  useEffect(() => {
    const fetchAgentDetails = async () => {
      try {
        const response = await fetch(`/api/agent/${id}`);
        const data = await response.json();
        if (response.ok) {
          setAgent(data);
        } else {
          setError(data.detail || 'Failed to load agent');
        }
      } catch (error) {
        setError('Failed to load agent details');
        console.error('Error fetching agent details:', error);
      } finally {
        setIsLoadingAgent(false);
      }
    };

    if (id) {
      fetchAgentDetails();
    }
  }, [id]);

  // Load chat history on mount
  useEffect(() => {
    const loadChatHistory = async () => {
      const userId = localStorage.getItem('userId');
      if (!userId || !id) return;

      try {
        const response = await fetch(`/api/agent/${id}/chat_history?user_id=${userId}`);
        if (!response.ok) {
          throw new Error('Failed to load chat history');
        }
        const data = await response.json();
        setMessages(id, data.messages || []);
      } catch (error) {
        console.error('Error loading chat history:', error);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadChatHistory();
  }, [id, setMessages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    const userId = localStorage.getItem('userId');
    if (!userId) {
      setError('Please log in to send messages');
      return;
    }

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage.trim(),
      created_at: new Date().toISOString()
    };
    addMessage(id, userMessage);
    setInputMessage('');
    
    // Send message and get response
    setIsLoading(true);
    try {
      const response = await sendMessage(id, inputMessage.trim(), userId);
      
      // Add agent response
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: response,
        created_at: new Date().toISOString()
      };
      addMessage(id, agentMessage);
    } catch (error) {
      logger.error('Error sending message:', error);
      setError(error instanceof Error ? error.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoadingAgent) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <LoadingDots className="text-primary" />
      </div>
    );
  }

  if (error || !agent) {
    return (
      <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle className="text-destructive">Error</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{error || 'Failed to load agent'}</p>
            <Button className="mt-4 w-full" onClick={() => window.location.href = '/explore'}>
              Return to Explore
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="flex-none">
        <Card className="border-0 shadow-none">
          <CardHeader className="pb-4">
            <div className="flex items-center gap-4">
              <Link href="/explore">
                <Button variant="ghost" size="icon" className="shrink-0">
                  <ArrowLeft className="w-5 h-5" />
                </Button>
              </Link>
              {agent.profile_photo_url ? (
                <div className="relative w-12 h-12 rounded-full overflow-hidden shrink-0">
                  <Image
                    src={agent.profile_photo_url}
                    alt={agent.expert_name}
                    fill
                    className="object-cover"
                  />
                </div>
              ) : (
                <div className="w-12 h-12 rounded-full bg-muted flex items-center justify-center shrink-0">
                  <User2 className="w-6 h-6 text-muted-foreground" />
                </div>
              )}
              <div className="min-w-0">
                <CardTitle className="truncate">{agent.expert_name}</CardTitle>
                <CardDescription className="truncate">
                  Created {new Date(agent.created_at).toLocaleDateString()}
                </CardDescription>
              </div>
            </div>
            <div className="text-sm text-muted-foreground mt-2">
              Status: {agent.status}
            </div>
          </CardHeader>
        </Card>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {isLoadingHistory ? (
          <div className="flex justify-center">
            <LoadingDots />
          </div>
        ) : currentMessages.length > 0 ? (
          currentMessages.map((message: Message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                <div className="text-xs opacity-70 mt-1">
                  {new Date(message.created_at).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center text-muted-foreground">
            No messages yet. Start a conversation!
          </div>
        )}
      </div>

      {/* Message Input */}
      <div className="flex-none p-4">
        <form onSubmit={handleSendMessage} className="flex gap-2">
          <Input
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading || !inputMessage.trim()}>
            {isLoading ? <LoadingDots /> : <Send className="w-4 h-4" />}
          </Button>
        </form>
      </div>
    </div>
  );
} 