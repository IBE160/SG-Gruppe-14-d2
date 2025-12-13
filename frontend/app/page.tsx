import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { hasEnvVars } from "@/lib/utils";
import Link from "next/link";
import { Suspense } from "react";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center">
      <div className="flex-1 w-full flex flex-col gap-20 items-center">
        <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
          <div className="w-full max-w-5xl flex justify-between items-center p-3 px-5 text-sm">
            <div className="flex gap-4 items-center">
              <Link href="/" className="text-lg font-bold">
                My Awesome App
              </Link>
              <Link
                href="/prompts"
                className="text-sm font-medium hover:underline"
              >
                Agent Prompts
              </Link>
              <Link
                href="/chat"
                className="text-sm font-medium hover:underline"
              >
                Chat
              </Link>
            </div>
            {!hasEnvVars ? (
              <EnvVarWarning />
            ) : (
              <Suspense>
                <AuthButton />
              </Suspense>
            )}
          </div>
        </nav>
        <div className="flex-1 flex flex-col max-w-5xl items-center justify-center p-5">
          <h2 className="text-4xl font-bold text-center">Welcome!</h2>
          <p className="text-center text-lg mt-4">
            Your clean slate for development.
          </p>
        </div>
      </div>
    </main>
  );
}
