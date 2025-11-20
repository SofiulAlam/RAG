import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="max-w-4xl text-center space-y-8">
        <h1 className="text-6xl font-bold tracking-tight">
          AI App Builder
        </h1>
        <p className="text-xl text-muted-foreground">
          Build web applications through natural language prompts.
          Powered by Claude AI with intelligent prompt enhancement and iterative development.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/dashboard">
            <Button size="lg">
              Get Started
            </Button>
          </Link>
          <Link href="/templates">
            <Button size="lg" variant="outline">
              Browse Templates
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
