'use client'

import { useState } from 'react'

interface CategoryPillsProps {
  categories: string[]
}

export default function CategoryPills({ categories }: CategoryPillsProps) {
  const [selectedCategory, setSelectedCategory] = useState('All')

  return (
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
  )
}

