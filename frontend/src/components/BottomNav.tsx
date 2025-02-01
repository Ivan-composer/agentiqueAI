"use client";

import { HomeIcon, SearchIcon, UserIcon } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

/**
 * BottomNav component provides mobile-first navigation between main app sections.
 * Uses Lucide icons and Next.js Link for client-side navigation.
 */
export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 w-full flex justify-around items-center bg-white border-t border-gray-200 pb-safe-area">
      {/* Explore */}
      <Link 
        href="/explore" 
        className={`flex flex-col items-center p-2 min-w-[64px] ${
          pathname === '/explore' ? 'text-blue-600' : 'text-gray-600'
        }`}
      >
        <HomeIcon className="w-6 h-6 mb-1" />
        <span className="text-xs">Explore</span>
      </Link>

      {/* AI Search */}
      <Link 
        href="/" 
        className={`flex flex-col items-center p-2 min-w-[64px] ${
          pathname === '/' ? 'text-blue-600' : 'text-gray-600'
        }`}
      >
        <SearchIcon className="w-6 h-6 mb-1" />
        <span className="text-xs">AI Search</span>
      </Link>

      {/* Profile */}
      <Link 
        href="/profile" 
        className={`flex flex-col items-center p-2 min-w-[64px] ${
          pathname === '/profile' ? 'text-blue-600' : 'text-gray-600'
        }`}
      >
        <UserIcon className="w-6 h-6 mb-1" />
        <span className="text-xs">Profile</span>
      </Link>
    </nav>
  );
} 