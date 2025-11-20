import { TemplateGrid } from "@/components/templates/TemplateGrid";

export default function TemplatesPage() {
  return (
    <div className="container mx-auto p-6 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Template Library</h1>
        <p className="text-muted-foreground">
          Start with pre-built templates for common applications
        </p>
      </div>

      <TemplateGrid />
    </div>
  );
}
