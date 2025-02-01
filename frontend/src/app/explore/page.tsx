"use client";

import { useState } from 'react';
import { PlusCircle, Loader2 } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LoadingDots } from '@/components/ui/loading-dots';

/**
 * Explore page component showing available AI agents and creation option.
 * Will integrate with backend /agents endpoint later.
 */
export default function ExplorePage() {
  const [isCreating, setIsCreating] = useState(false);
  const [telegramLink, setTelegramLink] = useState('');
  const [progress, setProgress] = useState(0);

  const handleCreateAgent = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!telegramLink.trim()) return;

    setIsCreating(true);
    try {
      // Simulate progress updates
      for (let i = 0; i <= 100; i += 20) {
        setProgress(i);
        await new Promise(resolve => setTimeout(resolve, 500));
      }
      
      // TODO: Integrate with backend POST /agent/create
      console.log('Creating agent with link:', telegramLink);
    } catch (error) {
      console.error('Error creating agent:', error);
    } finally {
      setIsCreating(false);
      setTelegramLink('');
      setProgress(0);
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
            <div className="space-y-2">
              <label htmlFor="telegram-link" className="text-sm text-muted-foreground">
                Telegram Channel Link
              </label>
              <Input
                id="telegram-link"
                type="text"
                value={telegramLink}
                onChange={(e) => setTelegramLink(e.target.value)}
                placeholder="https://t.me/yourchannel"
                disabled={isCreating}
              />
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

            <Button
              type="submit"
              disabled={isCreating}
              className="w-full"
            >
              {isCreating ? (
                <>
                  <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <PlusCircle className="w-5 h-5 mr-2" />
                  Create AI Agent
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Agent List - Placeholder */}
      <Card>
        <CardHeader>
          <CardTitle>Available Agents</CardTitle>
        </CardHeader>
        <CardContent>
          {isCreating ? (
            <div className="text-center py-8">
              <LoadingDots className="text-primary mx-auto mb-4" />
              <p className="text-muted-foreground">
                Creating your AI agent...
              </p>
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