import { ProjectList } from "@/components/dashboard/ProjectList";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function DashboardPage() {
  return (
    <div className="container mx-auto p-6 space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Your Projects</h1>
          <p className="text-muted-foreground">
            Create and manage your AI-generated applications
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </div>

      <ProjectList />
    </div>
  );
}
