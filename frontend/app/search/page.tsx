'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Search as SearchIcon, Loader2 } from 'lucide-react';
import { searchAgents } from '@/lib/api';
import type { SearchResult } from '@/lib/api';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      const searchResults = await searchAgents(query.trim());
      setResults(searchResults);
    } catch (err: any) {
      setError(err.message || 'Failed to perform search. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

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
          Search AI Agents
        </h1>
      </div>

      {/* Search Form */}
      <div className="max-w-4xl mx-auto p-4">
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-4">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search across all AI agents..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-[#0098EA] focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white px-6 py-2 rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <SearchIcon className="w-5 h-5" />
              )}
            </button>
          </div>
        </form>

        {/* Error Message */}
        {error && (
          <div className="text-red-500 text-sm p-3 bg-red-50 rounded-md border border-red-100 mb-4">
            {error}
          </div>
        )}

        {/* Results */}
        <div className="space-y-4">
          {results.length === 0 && query && !isLoading ? (
            <div className="text-center text-gray-500 py-8">
              No results found for "{query}"
            </div>
          ) : (
            results.map((result, index) => (
              <div
                key={index}
                className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                <h2 className="text-lg font-semibold text-gray-900 mb-2">
                  {result.title}
                </h2>
                <p className="text-gray-600 mb-3">{result.summary}</p>
                <a
                  href={result.source_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-[#0098EA] hover:underline text-sm"
                >
                  View Source →
                </a>
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
} 