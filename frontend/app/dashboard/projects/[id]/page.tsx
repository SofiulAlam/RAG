"use client";

import { EditorLayout } from "@/components/editor/EditorLayout";
import { use } from "react";

export default function ProjectPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);

  return <EditorLayout projectId={id} />;
}
