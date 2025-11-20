"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface EnhancePromptModalProps {
  open: boolean;
  onClose: () => void;
  originalPrompt: string;
  onUseEnhanced: (enhanced: string) => void;
}

export function EnhancePromptModal({
  open,
  onClose,
  originalPrompt,
  onUseEnhanced,
}: EnhancePromptModalProps) {
  const [enhancedPrompt, setEnhancedPrompt] = useState("");
  const [isEnhancing, setIsEnhancing] = useState(false);

  useEffect(() => {
    if (open && originalPrompt) {
      enhancePrompt();
    }
  }, [open, originalPrompt]);

  const enhancePrompt = async () => {
    setIsEnhancing(true);
    try {
      // TODO: Implement API call
      const response = await fetch("/api/prompts/enhance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: originalPrompt }),
      });

      if (!response.ok) throw new Error("Failed to enhance prompt");

      const data = await response.json();
      setEnhancedPrompt(data.enhanced);
    } catch (error) {
      console.error("Failed to enhance prompt:", error);
      setEnhancedPrompt(originalPrompt);
    } finally {
      setIsEnhancing(false);
    }
  };

  const handleUse = () => {
    onUseEnhanced(enhancedPrompt);
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle>Enhanced Prompt</DialogTitle>
          <DialogDescription>
            AI has enhanced your prompt with more details and structure
          </DialogDescription>
        </DialogHeader>

        <div className="grid grid-cols-2 gap-4 flex-1 overflow-auto">
          <div>
            <h3 className="text-sm font-semibold mb-2">Original</h3>
            <div className="p-3 bg-muted rounded-md text-sm whitespace-pre-wrap">
              {originalPrompt}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold mb-2">Enhanced</h3>
            {isEnhancing ? (
              <div className="flex items-center justify-center h-32">
                Enhancing prompt...
              </div>
            ) : (
              <Textarea
                value={enhancedPrompt}
                onChange={(e) => setEnhancedPrompt(e.target.value)}
                className="min-h-[200px]"
              />
            )}
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleUse} disabled={isEnhancing}>
            Use Enhanced Prompt
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
