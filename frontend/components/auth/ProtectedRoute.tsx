"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/lib/auth";

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const token = useAuthStore((state) => state.token);

  useEffect(() => {
    if (!token) {
      router.push("/login");
    }
  }, [token, router]);

  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p>Redirecting to login...</p>
      </div>
    );
  }

  return <>{children}</>;
}
