"use client";

import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

interface Project {
  id: string;
  name: string;
  framework: string;
  created_at: string;
  updated_at: string;
}

export function ProjectList() {
  const { data: projects, isLoading } = useQuery<Project[]>({
    queryKey: ["projects"],
    queryFn: async () => {
      // TODO: Implement API call
      return [];
    },
  });

  if (isLoading) {
    return <div>Loading projects...</div>;
  }

  if (!projects || projects.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>No projects yet</CardTitle>
          <CardDescription>
            Create your first project to get started
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {projects.map((project) => (
        <Link key={project.id} href={`/dashboard/projects/${project.id}`}>
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardHeader>
              <CardTitle>{project.name}</CardTitle>
              <CardDescription>{project.framework}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Updated {new Date(project.updated_at).toLocaleDateString()}
              </p>
            </CardContent>
          </Card>
        </Link>
      ))}
    </div>
  );
}
