'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { Plus } from 'lucide-react'
import BottomNav from '../bottom-nav'

const categories = [
  'All',
  'Investing',
  'Lifestyle',
  'Finance',
  'Popular',
  'Technology',
  'Art',
  'Music'
]

const popularCreators = Array(10).fill(null).map((_, i) => ({
  id: i,
  name: `Creator ${i + 1}`,
  description: 'AI Creator',
  imageUrl: `/placeholder.svg?height=100&width=100`
}))

const topCreatorsByCategory = {
  'Investing': Array(5).fill(null).map((_, i) => ({
    id: i + 10,
    name: `Investment Expert ${i + 1}`,
    description: 'Financial advice and market insights',
    imageUrl: `/placeholder.svg?height=200&width=200`
  }))
}

export default function ExplorePage() {
  const [selectedCategory, setSelectedCategory] = useState('All')

  return (
    <main className="min-h-screen bg-white text-black pb-20">
      <div className="sticky top-0 z-10 bg-white pt-4 pb-2 px-4">
        <h1 className="text-2xl font-bold text-center mb-4 font-['Inter']">Explore creators</h1>
        
        {/* Search Bar */}
        <div className="relative mb-4">
          <input
            type="text"
            placeholder="Search creators or topics"
            className="w-full bg-gray-100 text-black placeholder-gray-400 pl-10 pr-4 py-3 rounded-full focus:outline-none focus:ring-2 focus:ring-[#0098EA]"
          />
          <svg
            className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>

        {/* Category Pills */}
        <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-1.5 rounded-full whitespace-nowrap text-sm ${
                selectedCategory === category
                  ? 'bg-[#0098EA] text-white'
                  : 'bg-gray-100 text-black hover:bg-gray-200'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {/* Create AI-Spirit Button */}
      <div className="px-4 mt-4 mb-8">
        <Link
          href="/create-spirit"
          className="flex items-center justify-center gap-3 w-full bg-[#08C6C9] hover:bg-[#06a4a6] text-white py-4 rounded-xl text-lg font-['Inter'] font-semibold transition-colors"
        >
          <Plus className="w-7 h-7" />
          Make AI-Spirit of any creator
        </Link>
      </div>

      <div className="px-4 space-y-8">
        {/* Popular Creators Section */}
        <section>
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            Popular this week
            <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
              <path
                fillRule="evenodd"
                d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                clipRule="evenodd"
              />
            </svg>
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
            {popularCreators.map((creator) => (
              <Link
                key={creator.id}
                href={`/creator/${creator.id}`}
                className="flex-shrink-0 w-[200px]"
              >
                <div className="relative aspect-square mb-2">
                  <Image
                    src={creator.imageUrl}
                    alt={creator.name}
                    fill
                    className="object-cover rounded-xl"
                  />
                </div>
                <h3 className="font-semibold text-black">{creator.name}</h3>
                <p className="text-sm text-gray-600">{creator.description}</p>
              </Link>
            ))}
          </div>
        </section>

        {/* Category Sections */}
        {Object.entries(topCreatorsByCategory).map(([category, creators]) => (
          <section key={category}>
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              {category}
              <svg className="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            </h2>
            <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
              {creators.map((creator) => (
                <Link
                  key={creator.id}
                  href={`/creator/${creator.id}`}
                  className="flex-shrink-0 w-[300px]"
                >
                  <div className="relative aspect-square mb-2">
                    <Image
                      src={creator.imageUrl}
                      alt={creator.name}
                      fill
                      className="object-cover rounded-xl"
                    />
                  </div>
                  <h3 className="font-semibold text-black">{creator.name}</h3>
                  <p className="text-sm text-gray-600">{creator.description}</p>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>

      <BottomNav />
    </main>
  )
} 