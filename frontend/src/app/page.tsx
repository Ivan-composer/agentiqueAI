"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { SearchIcon } from 'lucide-react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

/**
 * Home page component featuring the AI Search interface.
 * Allows users to search across all AI agents.
 */
export default function Home() {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search-results?query=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center">
      <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-green-400 to-blue-500 bg-clip-text text-transparent">
        Agentique AI
      </h1>
      
      <p className="text-xl mb-8 text-gray-700">
        Solve any problem with AI-Agents
      </p>
      
      <p className="text-sm mb-8 text-muted-foreground">
        We'll pick the most relevant agents to help you
      </p>

      <form onSubmit={handleSearch} className="w-full max-w-md">
        <div className="relative">
          <Input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything..."
            className="pr-12"
          />
          <Button 
            type="submit"
            variant="ghost" 
            size="icon"
            className="absolute right-2 top-1/2 -translate-y-1/2"
          >
            <SearchIcon className="w-5 h-5" />
          </Button>
        </div>
      </form>
    </div>
  );
}
