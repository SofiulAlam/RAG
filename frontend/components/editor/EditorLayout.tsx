"use client";

import { useState } from "react";
import { FileTree } from "./FileTree";
import { MonacoEditor } from "./MonacoEditor";
import { Preview } from "./Preview";
import { ChatInterface } from "../chat/ChatInterface";

interface EditorLayoutProps {
  projectId: string;
}

export function EditorLayout({ projectId }: EditorLayoutProps) {
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  return (
    <div className="h-screen flex flex-col">
      {/* Top Navigation */}
      <header className="h-14 border-b flex items-center px-4 justify-between">
        <h1 className="text-lg font-semibold">AI App Builder</h1>
        <div className="flex gap-2">
          {/* TODO: Add settings, deploy buttons */}
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - File Tree */}
        <aside className="w-64 border-r overflow-auto">
          <FileTree
            projectId={projectId}
            selectedFile={selectedFile}
            onFileSelect={setSelectedFile}
          />
        </aside>

        {/* Center - Editor */}
        <main className="flex-1 flex flex-col">
          <div className="flex-1 overflow-hidden">
            <MonacoEditor
              projectId={projectId}
              file={selectedFile}
            />
          </div>

          {/* Bottom - Chat */}
          <div className="h-96 border-t">
            <ChatInterface projectId={projectId} />
          </div>
        </main>

        {/* Right Sidebar - Preview */}
        <aside className="w-1/3 border-l overflow-hidden">
          <Preview projectId={projectId} />
        </aside>
      </div>
    </div>
  );
}
