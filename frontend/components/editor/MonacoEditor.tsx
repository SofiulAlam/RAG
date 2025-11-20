"use client";

import Editor from "@monaco-editor/react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";

interface MonacoEditorProps {
  projectId: string;
  file: string | null;
}

export function MonacoEditor({ projectId, file }: MonacoEditorProps) {
  const queryClient = useQueryClient();
  const [localContent, setLocalContent] = useState<string>("");

  const { data: fileContent, isLoading } = useQuery({
    queryKey: ["file", projectId, file],
    queryFn: async () => {
      if (!file) return null;
      // TODO: Implement API call
      const response = await fetch(`/api/projects/${projectId}/files/${file}`);
      if (!response.ok) throw new Error("Failed to fetch file");
      return response.json();
    },
    enabled: !!file,
  });

  const updateFileMutation = useMutation({
    mutationFn: async (content: string) => {
      if (!file) return;
      // TODO: Implement API call
      const response = await fetch(`/api/projects/${projectId}/files/${file}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content }),
      });
      if (!response.ok) throw new Error("Failed to update file");
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["file", projectId, file] });
    },
  });

  useEffect(() => {
    if (fileContent) {
      setLocalContent(fileContent.content);
    }
  }, [fileContent]);

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setLocalContent(value);
      // Debounce save
      const timer = setTimeout(() => {
        updateFileMutation.mutate(value);
      }, 500);
      return () => clearTimeout(timer);
    }
  };

  if (!file) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground">
        Select a file to start editing
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center">
        Loading file...
      </div>
    );
  }

  const getLanguage = (filename: string) => {
    const ext = filename.split(".").pop();
    const languageMap: Record<string, string> = {
      ts: "typescript",
      tsx: "typescript",
      js: "javascript",
      jsx: "javascript",
      json: "json",
      css: "css",
      html: "html",
      md: "markdown",
      py: "python",
    };
    return languageMap[ext || ""] || "plaintext";
  };

  return (
    <Editor
      height="100%"
      language={getLanguage(file)}
      value={localContent}
      onChange={handleEditorChange}
      theme="vs-dark"
      options={{
        minimap: { enabled: true },
        fontSize: 14,
        formatOnPaste: true,
        formatOnType: true,
        automaticLayout: true,
        scrollBeyondLastLine: false,
        wordWrap: "on",
      }}
    />
  );
}
