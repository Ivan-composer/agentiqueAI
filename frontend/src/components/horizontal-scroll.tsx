interface HorizontalScrollProps {
  children: React.ReactNode
}

export default function HorizontalScroll({ children }: HorizontalScrollProps) {
  return (
    <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide scroll-smooth">
      {children}
    </div>
  )
}

