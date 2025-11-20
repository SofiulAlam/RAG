"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { MessageList } from "./MessageList";
import { PromptInput } from "./PromptInput";

interface ChatInterfaceProps {
  projectId: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export function ChatInterface({ projectId }: ChatInterfaceProps) {
  const { data: messages, isLoading } = useQuery<Message[]>({
    queryKey: ["chat", projectId],
    queryFn: async () => {
      // TODO: Implement API call
      const response = await fetch(`/api/projects/${projectId}/chat`);
      if (!response.ok) throw new Error("Failed to fetch messages");
      return response.json();
    },
  });

  const [isGenerating, setIsGenerating] = useState(false);

  const handleSendMessage = async (content: string) => {
    setIsGenerating(true);
    try {
      // TODO: Implement message sending with streaming
      const response = await fetch(`/api/projects/${projectId}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      });

      if (!response.ok) throw new Error("Failed to send message");
    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-auto">
        <MessageList messages={messages || []} isLoading={isLoading} />
      </div>

      <div className="border-t p-4">
        <PromptInput
          onSend={handleSendMessage}
          disabled={isGenerating}
        />
      </div>
    </div>
  );
}
