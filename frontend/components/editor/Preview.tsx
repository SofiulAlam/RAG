"use client";

import { useEffect, useRef, useState } from "react";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";

interface PreviewProps {
  projectId: string;
}

export function Preview({ projectId }: PreviewProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // TODO: Get preview URL from API
    // For now, use placeholder
    setPreviewUrl(`http://localhost:3001?project=${projectId}`);
  }, [projectId]);

  const handleRefresh = () => {
    if (iframeRef.current) {
      iframeRef.current.src = previewUrl;
    }
  };

  return (
    <div className="h-full flex flex-col">
      <div className="h-12 border-b flex items-center justify-between px-4">
        <h3 className="text-sm font-semibold">Preview</h3>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleRefresh}
        >
          <RefreshCw className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex-1 bg-white">
        {previewUrl ? (
          <iframe
            ref={iframeRef}
            src={previewUrl}
            className="w-full h-full border-0"
            sandbox="allow-scripts allow-same-origin"
            onLoad={() => setIsLoading(false)}
          />
        ) : (
          <div className="h-full flex items-center justify-center text-muted-foreground">
            No preview available
          </div>
        )}

        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-background/50">
            Loading preview...
          </div>
        )}
      </div>
    </div>
  );
}
