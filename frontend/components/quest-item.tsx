import QuestIcon from '@/components/quest-icon'
import TokenIcon from '@/components/token-icon'

interface QuestItemProps {
  name: string
  reward: number
}

export default function QuestItem({ name, reward }: QuestItemProps) {
  return (
    <div className="rounded-2xl bg-white shadow-sm border border-gray-100">
      <div className="p-4">
        <div className="flex items-center gap-3 mb-3">
          <QuestIcon className="w-12 h-12" />
          <h3 className="text-lg font-semibold">{name}</h3>
        </div>
        <div className="bg-[#F1F5F9] rounded-xl py-3 px-4">
          <div className="flex items-center justify-center gap-2">
            <span className="text-[#0098EA] text-xl font-semibold">+{reward}</span>
            <TokenIcon className="w-5 h-5" />
          </div>
        </div>
      </div>
    </div>
  )
}

