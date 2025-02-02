import './globals.css';
import { Inter } from 'next/font/google';
import { ClientLayout } from '@/components/ClientLayout';
import type { Metadata } from 'next';

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
      <body className={inter.className}>
        <ClientLayout>
          {children}
        </ClientLayout>
      </body>
    </html>
  );
}
