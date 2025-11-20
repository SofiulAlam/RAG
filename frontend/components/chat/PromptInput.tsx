"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Send, Sparkles } from "lucide-react";
import { EnhancePromptModal } from "./EnhancePromptModal";

interface PromptInputProps {
  onSend: (content: string) => void;
  disabled?: boolean;
}

export function PromptInput({ onSend, disabled }: PromptInputProps) {
  const [prompt, setPrompt] = useState("");
  const [showEnhance, setShowEnhance] = useState(false);

  const handleSend = () => {
    if (prompt.trim()) {
      onSend(prompt);
      setPrompt("");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleEnhance = () => {
    setShowEnhance(true);
  };

  const handleEnhancedPrompt = (enhanced: string) => {
    setPrompt(enhanced);
    setShowEnhance(false);
  };

  return (
    <>
      <div className="relative">
        <Textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Describe what you want to build..."
          className="pr-24 min-h-[80px]"
          disabled={disabled}
        />

        <div className="absolute bottom-2 right-2 flex gap-2">
          <Button
            size="sm"
            variant="ghost"
            onClick={handleEnhance}
            disabled={!prompt.trim() || disabled}
            title="Enhance Prompt"
          >
            <Sparkles className="h-4 w-4" />
          </Button>

          <Button
            size="sm"
            onClick={handleSend}
            disabled={!prompt.trim() || disabled}
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <EnhancePromptModal
        open={showEnhance}
        onClose={() => setShowEnhance(false)}
        originalPrompt={prompt}
        onUseEnhanced={handleEnhancedPrompt}
      />
    </>
  );
}
