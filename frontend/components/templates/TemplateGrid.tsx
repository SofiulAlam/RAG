"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Template {
  id: string;
  name: string;
  category: string;
  description: string;
  framework: string;
  preview_image?: string;
}

export function TemplateGrid() {
  const { data: templates, isLoading } = useQuery<Template[]>({
    queryKey: ["templates"],
    queryFn: async () => {
      // TODO: Implement API call
      return [];
    },
  });

  if (isLoading) {
    return <div>Loading templates...</div>;
  }

  if (!templates || templates.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>No templates available</CardTitle>
          <CardDescription>
            Templates will be added soon
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      {templates.map((template) => (
        <Card key={template.id} className="overflow-hidden">
          {template.preview_image && (
            <div className="aspect-video bg-muted">
              <img
                src={template.preview_image}
                alt={template.name}
                className="w-full h-full object-cover"
              />
            </div>
          )}

          <CardHeader>
            <CardTitle>{template.name}</CardTitle>
            <CardDescription>{template.category}</CardDescription>
          </CardHeader>

          <CardContent>
            <p className="text-sm text-muted-foreground mb-4">
              {template.description}
            </p>
            <Button className="w-full">Use Template</Button>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
