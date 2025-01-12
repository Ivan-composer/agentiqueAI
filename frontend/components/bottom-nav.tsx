'use client'

import Link from 'next/link'
import { User } from 'lucide-react'
import { usePathname } from 'next/navigation'

interface BottomNavProps {
  currentPage?: 'explore' | 'ai-search' | 'profile'
}

export default function BottomNav({ currentPage }: BottomNavProps) {
  const pathname = usePathname()
  const isExploreActive = currentPage === 'explore' || pathname === '/explore' || pathname?.startsWith('/creator/') || pathname?.startsWith('/create-agent')
  const isAISearchActive = currentPage === 'ai-search' || pathname === '/' || pathname?.startsWith('/ai-search')
  const isProfileActive = currentPage === 'profile' || pathname === '/profile'

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#F8FAFC] px-6 py-4">
      <div className="max-w-[280px] mx-auto flex justify-between items-center">
        <Link
          href="/explore"
          className={`flex flex-col items-center gap-1.5 transition-colors ${
            isExploreActive ? 'text-[#0098EA]' : 'text-[#435A6B] hover:text-[#08C6C9]'
          }`}
        >
          <svg width="32" height="32" viewBox="0 0 108 87" fill="none" xmlns="http://www.w3.org/2000/svg" className="stroke-current" strokeWidth="6">
            <path d="M69.8748 70.5L103.509 39.5659C103.854 39.212 103.854 38.6383 103.509 38.2845L101.605 36.3268C97.4924 32.1003 97.4924 25.2477 101.605 21.0212C101.879 20.7394 101.879 20.2826 101.605 20.0008L92.4211 10.5621C92.147 10.2803 91.7025 10.2803 91.4283 10.5621C87.3161 14.7886 80.6489 14.7886 76.5367 10.562L74.8137 8.79123C74.4762 8.44426 73.9288 8.44426 73.5912 8.79123L52.9287 30.0281" />
            <path d="M27.0194 58.3341L8.1786 38.8535L8.47464 38.5474C13.1808 33.6815 13.6477 26.1248 9.8755 20.7249L16.0988 14.2903C21.3795 18.117 28.7398 17.5942 33.4522 12.7217L33.802 12.36L52.4836 31.6759L78.9575 60.1134L59.4458 81.9644C56.7673 84.6922 52.4994 84.6791 49.8361 81.9254L27.0194 58.3341Z" />
          </svg>
          <span className="text-sm font-semibold font-['SF Pro Display']">Explore</span>
        </Link>
        <Link
          href="/"
          className={`flex flex-col items-center gap-1.5 transition-colors ${
            isAISearchActive ? 'text-[#0098EA]' : 'text-[#435A6B] hover:text-[#08C6C9]'
          }`}
        >
          <svg width="32" height="32" viewBox="0 0 77 74" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-current">
            <path fillRule="evenodd" clipRule="evenodd" d="M48.6495 6.78607C49.8611 5.54752 49.5223 3.48931 47.9082 2.85961C44.0028 1.3361 39.7535 0.5 35.3088 0.5C16.1532 0.5 0.625 16.0304 0.625 35.1875C0.625 54.3447 16.1532 69.8751 35.3088 69.8751C43.9888 69.8751 51.9239 66.6863 58.007 61.4163L69.3571 72.7677C70.3334 73.744 71.9163 73.7441 72.8927 72.7679C73.869 71.7916 73.8691 70.2087 72.8929 69.2323L61.5418 57.88C65.7506 53.0178 68.629 46.713 69.6147 39.947C69.9273 37.8016 67.5381 36.5373 65.7759 37.8002C65.1617 38.2404 64.7697 38.9226 64.6566 39.6697C62.496 53.9391 50.1792 64.8751 35.3088 64.8751C18.9152 64.8751 5.625 51.5838 5.625 35.1875C5.625 18.7913 18.9152 5.5 35.3088 5.5C38.9806 5.5 42.4966 6.16674 45.7425 7.38578C46.7495 7.76397 47.8973 7.55501 48.6495 6.78607Z" fill="currentColor"/>
            <path d="M43.125 19.8889C52.083 17.619 56.562 13.0794 58.8015 4C61.041 13.0794 65.52 17.619 74.4779 19.8889C65.52 22.1587 61.041 26.6984 58.8015 35.7778C56.562 26.6984 52.083 22.1587 43.125 19.8889Z" stroke="currentColor" strokeWidth="5" strokeLinejoin="round"/>
          </svg>
          <span className="text-sm font-semibold font-['SF Pro Display']">AI Search</span>
        </Link>
        <Link
          href="/profile"
          className={`flex flex-col items-center gap-1.5 transition-colors ${
            isProfileActive ? 'text-[#0098EA]' : 'text-[#435A6B] hover:text-[#08C6C9]'
          }`}
        >
          <User className="w-8 h-8" strokeWidth={1.5} />
          <span className="text-sm font-semibold font-['SF Pro Display']">Profile</span>
        </Link>
      </div>
    </nav>
  )
}

