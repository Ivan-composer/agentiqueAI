import CategoryPills from '@/components/category-pills'
import CreatorCard from '@/components/creator-card'
import HorizontalScroll from '@/components/horizontal-scroll'
import SearchBar from '@/components/search-bar'
import SectionHeader from '@/components/section-header'
import BottomNav from '@/components/bottom-nav'
import { Plus } from 'lucide-react'
import Link from 'next/link'

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
  return (
    <main className="min-h-screen bg-white text-black pb-20">
      <div className="sticky top-0 z-10 bg-white pt-4 pb-2 px-4">
        <h1 className="text-2xl font-bold text-center mb-4 font-['Inter']">Explore creators</h1>
        <SearchBar />
        <CategoryPills categories={categories} />
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
        <section>
          <SectionHeader title="Popular this week" />
          <HorizontalScroll>
            {popularCreators.map((creator) => (
              <CreatorCard
                key={creator.id}
                variant="small"
                {...creator}
              />
            ))}
          </HorizontalScroll>
        </section>

        {Object.entries(topCreatorsByCategory).map(([category, creators]) => (
          <section key={category}>
            <SectionHeader title={category} />
            <HorizontalScroll>
              {creators.map((creator) => (
                <CreatorCard
                  key={creator.id}
                  variant="large"
                  {...creator}
                />
              ))}
            </HorizontalScroll>
          </section>
        ))}
      </div>
      <BottomNav />
    </main>
  )
}

