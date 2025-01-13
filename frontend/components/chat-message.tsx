import Image from 'next/image'

interface MessageProps {
  message: {
    content: string
    role: 'user' | 'assistant'
  }
  creator: {
    name: string
    imageUrl: string
  }
}

export default function ChatMessage({ message, creator }: MessageProps) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="bg-[#F1F5F9] text-black rounded-2xl rounded-tr-sm px-4 py-3 max-w-[80%]">
          {message.content}
        </div>
        <div className="text-sm text-gray-500 self-end ml-2">You</div>
      </div>
    )
  }

  return (
    <div className="flex gap-2">
      <Image
        src={creator.imageUrl}
        alt={creator.name}
        width={32}
        height={32}
        className="rounded-full self-end"
      />
      <div className="flex-1">
        <div className="text-sm text-gray-500 mb-1">{creator.name} AI-agent</div>
        <div className="bg-[#EFF6FF] rounded-2xl rounded-tl-sm px-4 py-3">
          {message.content}
        </div>
      </div>
    </div>
  )
}

