"use client";

import { Message } from "./ChatInterface";
import { cn } from "@/lib/utils";

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        Loading messages...
      </div>
    );
  }

  if (messages.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center space-y-2">
          <p className="text-lg font-semibold">Start building your app</p>
          <p className="text-sm">
            Describe what you want to build and I'll help you create it
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      {messages.map((message) => (
        <div
          key={message.id}
          className={cn(
            "flex",
            message.role === "user" ? "justify-end" : "justify-start"
          )}
        >
          <div
            className={cn(
              "max-w-[80%] rounded-lg px-4 py-2",
              message.role === "user"
                ? "bg-primary text-primary-foreground"
                : "bg-muted"
            )}
          >
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
