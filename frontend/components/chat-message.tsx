import React from 'react';
import { ChatMessage as ChatMessageType } from '@/lib/api';
import { cn } from '@/lib/utils';
import Image from 'next/image'

interface ChatMessageProps extends ChatMessageType {
  className?: string;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ role, content, className }) => {
  const isUser = role === 'user';

  return (
    <div className={cn(
      'flex w-full',
      isUser ? 'justify-end' : 'justify-start',
      className
    )}>
      <div className={cn(
        'max-w-[80%] rounded-2xl px-4 py-2',
        isUser ? 'bg-[#0098EA] text-white' : 'bg-gray-100 text-gray-900'
      )}>
        <p className="text-sm whitespace-pre-wrap break-words">{content}</p>
      </div>
    </div>
  );
};

export default ChatMessage;

