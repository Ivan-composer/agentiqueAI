import { ChevronRight } from 'lucide-react'

interface SectionHeaderProps {
  title: string
}

export default function SectionHeader({ title }: SectionHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-4">
      <h2 className="text-xl font-semibold flex items-center gap-2">
        {title}
        <ChevronRight className="w-5 h-5" />
      </h2>
    </div>
  )
}

