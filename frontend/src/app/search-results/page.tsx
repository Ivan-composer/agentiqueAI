"use client";

import { useSearchParams } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MessageCircle, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

/**
 * Search Results page showing AI agents matching the user's query.
 * Will integrate with backend /search endpoint later.
 */
export default function SearchResultsPage() {
  const searchParams = useSearchParams();
  const query = searchParams.get('query') || '';

  // TODO: Replace with real API call
  const mockResults = [
    {
      id: '1',
      name: 'Marketing Expert',
      description: 'Expert in digital marketing and growth strategies',
      relevanceScore: 0.92,
      credits: 5
    },
    {
      id: '2',
      name: 'Tech Advisor',
      description: 'Specialized in software development and architecture',
      relevanceScore: 0.85,
      credits: 5
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Link href="/">
            <Button variant="ghost" size="icon">
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
          <h1 className="text-2xl font-bold">Search Results</h1>
        </div>
        <p className="text-muted-foreground">
          Showing AI agents that can help with: <span className="font-medium text-foreground">"{query}"</span>
        </p>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {mockResults.map((agent) => (
          <Card key={agent.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg">{agent.name}</CardTitle>
                  <CardDescription className="mt-1">
                    {agent.description}
                  </CardDescription>
                </div>
                <div className="text-sm text-muted-foreground">
                  {Math.round(agent.relevanceScore * 100)}% match
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center">
                <div className="text-sm text-muted-foreground">
                  {agent.credits} credits per message
                </div>
                <Link href={`/agent/${agent.id}`}>
                  <Button>
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Start Chat
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {mockResults.length === 0 && (
        <Card>
          <CardContent className="text-center py-8">
            <p className="text-muted-foreground">
              No AI agents found matching your query. Try a different search term.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
} 