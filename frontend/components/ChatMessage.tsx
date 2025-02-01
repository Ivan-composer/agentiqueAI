import { cn } from '@/lib/utils';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  className?: string;
}

export function ChatMessage({ role, content, className }: ChatMessageProps) {
  return (
    <div
      className={cn(
        'flex w-full items-start gap-4 p-4',
        role === 'user' ? 'bg-white' : 'bg-gray-50',
        className
      )}
    >
      <div
        className={cn(
          'flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow',
          role === 'user'
            ? 'bg-white text-gray-900'
            : 'bg-gradient-to-r from-[#08C6C9] to-[#0098EA] text-white'
        )}
      >
        {role === 'user' ? 'U' : 'A'}
      </div>
      <div className="flex-1 space-y-2">
        <p className="text-sm font-medium">
          {role === 'user' ? 'You' : 'AI Assistant'}
        </p>
        <div className="prose prose-sm max-w-none">
          <p>{content}</p>
        </div>
      </div>
    </div>
  );
} 