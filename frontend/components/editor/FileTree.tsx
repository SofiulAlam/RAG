"use client";

import { useQuery } from "@tanstack/react-query";
import { ChevronDown, ChevronRight, File, Folder, Lock, Unlock } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/utils";

interface FileTreeProps {
  projectId: string;
  selectedFile: string | null;
  onFileSelect: (file: string) => void;
}

interface FileNode {
  path: string;
  name: string;
  type: "file" | "directory";
  is_locked?: boolean;
  children?: FileNode[];
}

export function FileTree({ projectId, selectedFile, onFileSelect }: FileTreeProps) {
  const { data: files, isLoading } = useQuery<FileNode[]>({
    queryKey: ["files", projectId],
    queryFn: async () => {
      // TODO: Implement API call
      const response = await fetch(`/api/projects/${projectId}/files`);
      if (!response.ok) throw new Error("Failed to fetch files");
      return response.json();
    },
  });

  if (isLoading) {
    return <div className="p-4">Loading files...</div>;
  }

  return (
    <div className="p-2">
      <h3 className="text-sm font-semibold mb-2 px-2">Files</h3>
      <div className="space-y-1">
        {files?.map((file) => (
          <FileTreeNode
            key={file.path}
            node={file}
            selectedFile={selectedFile}
            onFileSelect={onFileSelect}
            level={0}
          />
        ))}
      </div>
    </div>
  );
}

function FileTreeNode({
  node,
  selectedFile,
  onFileSelect,
  level,
}: {
  node: FileNode;
  selectedFile: string | null;
  onFileSelect: (file: string) => void;
  level: number;
}) {
  const [isExpanded, setIsExpanded] = useState(true);
  const isSelected = selectedFile === node.path;

  if (node.type === "directory") {
    return (
      <div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center w-full px-2 py-1 hover:bg-accent rounded-sm text-sm"
          style={{ paddingLeft: `${level * 12 + 8}px` }}
        >
          {isExpanded ? (
            <ChevronDown className="h-4 w-4 mr-1" />
          ) : (
            <ChevronRight className="h-4 w-4 mr-1" />
          )}
          <Folder className="h-4 w-4 mr-2 text-blue-500" />
          {node.name}
        </button>
        {isExpanded && node.children && (
          <div>
            {node.children.map((child) => (
              <FileTreeNode
                key={child.path}
                node={child}
                selectedFile={selectedFile}
                onFileSelect={onFileSelect}
                level={level + 1}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

  return (
    <button
      onClick={() => onFileSelect(node.path)}
      className={cn(
        "flex items-center w-full px-2 py-1 hover:bg-accent rounded-sm text-sm",
        isSelected && "bg-accent"
      )}
      style={{ paddingLeft: `${level * 12 + 20}px` }}
    >
      <File className="h-4 w-4 mr-2 text-gray-500" />
      <span className="flex-1 text-left">{node.name}</span>
      {node.is_locked ? (
        <Lock className="h-3 w-3 text-muted-foreground" />
      ) : null}
    </button>
  );
}
