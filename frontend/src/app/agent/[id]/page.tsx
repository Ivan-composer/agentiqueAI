"use client";

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Send, Bot, User } from 'lucide-react';
import Link from 'next/link';
import { useChatStore, type Message, sendMessage, fetchChatHistory } from '@/lib/chat-service';
import { LoadingDots } from '@/components/ui/loading-dots';

/**
 * Agent Chat page for interacting with a specific AI agent.
 * Will integrate with backend /agent/{id}/chat endpoint later.
 */
export default function AgentChatPage() {
  const { id } = useParams();
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { messages, addMessage, setMessages } = useChatStore();
  const [agent, setAgent] = useState<{
    id: string;
    expert_name: string;
    status: string;
    created_at: string;
  } | null>(null);
  const [isLoadingAgent, setIsLoadingAgent] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch agent details
  useEffect(() => {
    const fetchAgentDetails = async () => {
      try {
        const response = await fetch(`/api/agent/${id}`);
        const data = await response.json();
        if (response.ok) {
          setAgent(data);
        } else {
          setError(data.detail || 'Failed to load agent details');
        }
      } catch (error) {
        setError('Failed to load agent details');
        console.error('Error fetching agent details:', error);
      } finally {
        setIsLoadingAgent(false);
      }
    };

    fetchAgentDetails();
  }, [id]);

  // Load chat history
  useEffect(() => {
    const loadHistory = async () => {
      const history = await fetchChatHistory(id as string);
      setMessages(id as string, history);
    };
    loadHistory();
  }, [id, setMessages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };
    addMessage(id as string, userMessage);
    setInputMessage('');
    
    // Send message and get response
    setIsLoading(true);
    try {
      const response = await sendMessage(id as string, userMessage.content);
      
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'agent',
        content: response,
        timestamp: new Date()
      };
      addMessage(id as string, agentMessage);
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const currentMessages = messages[id as string] || [];

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
            <div className="flex items-center gap-2">
              <Link href="/explore">
                <Button variant="ghost" size="icon" className="shrink-0">
                  <ArrowLeft className="w-5 h-5" />
                </Button>
              </Link>
              <div className="min-w-0">
                <CardTitle className="truncate">{agent.expert_name}</CardTitle>
                <CardDescription className="truncate">Created {new Date(agent.created_at).toLocaleDateString()}</CardDescription>
              </div>
            </div>
            <div className="text-sm text-muted-foreground mt-2">
              Status: {agent.status}
            </div>
          </CardHeader>
        </Card>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4 px-1 md:px-2">
        {currentMessages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-3 ${
              msg.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {msg.role === 'agent' && (
              <Bot className="w-6 h-6 text-primary flex-none" />
            )}
            <div
              className={`rounded-lg px-4 py-2 max-w-[85%] break-words ${
                msg.role === 'user'
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted'
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
              <p className="text-xs opacity-70 mt-1">
                {new Date(msg.timestamp).toLocaleTimeString()}
              </p>
            </div>
            {msg.role === 'user' && (
              <User className="w-6 h-6 text-primary flex-none" />
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex gap-3">
            <Bot className="w-6 h-6 text-primary flex-none" />
            <div className="bg-muted rounded-lg px-4 py-3">
              <LoadingDots className="text-primary" />
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="flex-none pt-4">
        <Card className="border-0 shadow-none">
          <CardContent>
            <form onSubmit={handleSendMessage} className="flex gap-2">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message..."
                disabled={isLoading}
                className="flex-1"
              />
              <Button 
                type="submit" 
                disabled={isLoading || !inputMessage.trim()}
                className="shrink-0"
              >
                <Send className="w-4 h-4" />
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
} 