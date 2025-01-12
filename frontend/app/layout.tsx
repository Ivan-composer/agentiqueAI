import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Agentique AI',
  description: 'Consult from AI Creators',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
