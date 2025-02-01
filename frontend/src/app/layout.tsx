import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { BottomNav } from '@/components/BottomNav';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Agentique AI',
  description: 'AI-powered platform for personalized consultations with AI-twins of content creators',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen relative pb-16`}>
        <main className="container mx-auto px-4 py-4">
          {children}
        </main>
        <BottomNav />
      </body>
    </html>
  );
}
