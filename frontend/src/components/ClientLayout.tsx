"use client";

import { BottomNav } from '@/components/BottomNav';

export function ClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <main className="container mx-auto px-4 pt-4 pb-20">
        {children}
      </main>
      <BottomNav />
    </>
  );
} 