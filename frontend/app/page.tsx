"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Sparkles,
  Zap,
  Code2,
  Rocket,
  Shield,
  Cpu,
  ArrowRight,
  Check,
  Star,
  Github,
  Terminal,
  Layers,
  Globe
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-slate-950 dark:via-blue-950 dark:to-purple-950">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/20">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl gradient-primary flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-display font-bold">AI App Builder</span>
            </div>

            <div className="hidden md:flex items-center gap-8">
              <Link href="#features" className="text-sm font-medium hover:text-primary transition-colors">
                Features
              </Link>
              <Link href="#templates" className="text-sm font-medium hover:text-primary transition-colors">
                Templates
              </Link>
              <Link href="#pricing" className="text-sm font-medium hover:text-primary transition-colors">
                Pricing
              </Link>
              <Link href="/templates" className="text-sm font-medium hover:text-primary transition-colors">
                Docs
              </Link>
            </div>

            <div className="flex items-center gap-3">
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="sm" className="gradient-primary text-white border-0 shine">
                  Get Started
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-8">
            {/* Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-purple-200/50 dark:border-purple-800/50 animate-float">
              <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
              <span className="text-sm font-medium">Powered by Claude 3.5 Sonnet</span>
            </div>

            {/* Headline */}
            <h1 className="text-6xl md:text-7xl lg:text-8xl font-display font-bold tracking-tight">
              Build Apps with
              <br />
              <span className="gradient-text">Natural Language</span>
            </h1>

            {/* Subheadline */}
            <p className="text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
              Transform your ideas into production-ready web applications.
              Just describe what you want to build, and watch AI create it instantly.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link href="/signup">
                <Button size="lg" className="gradient-primary text-white border-0 text-lg px-8 py-6 shine animate-glow">
                  <Rocket className="w-5 h-5 mr-2" />
                  Start Building Free
                </Button>
              </Link>
              <Link href="/templates">
                <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                  <Layers className="w-5 h-5 mr-2" />
                  Browse Templates
                </Button>
              </Link>
            </div>

            {/* Social Proof */}
            <div className="flex items-center justify-center gap-6 pt-8 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-500" />
                <span>No credit card required</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-500" />
                <span>Free forever</span>
              </div>
              <div className="flex items-center gap-2">
                <Check className="w-4 h-4 text-green-500" />
                <span>Open source</span>
              </div>
            </div>
          </div>

          {/* Hero Image/Demo */}
          <div className="mt-20 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-blue-500/20 blur-3xl rounded-full" />
            <div className="relative glass rounded-2xl p-8 border-2 border-white/20">
              <div className="bg-slate-900 rounded-xl overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-3 bg-slate-800 border-b border-slate-700">
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500" />
                    <div className="w-3 h-3 rounded-full bg-green-500" />
                  </div>
                  <span className="text-sm text-slate-400 ml-4">AI App Builder</span>
                </div>
                <div className="p-6 text-left">
                  <div className="flex items-start gap-3">
                    <Terminal className="w-5 h-5 text-green-400 mt-1" />
                    <div className="flex-1 space-y-2">
                      <p className="text-slate-300 font-mono text-sm">
                        <span className="text-green-400">$</span> Build a modern SaaS dashboard with user analytics
                      </p>
                      <div className="flex items-center gap-2 text-slate-500 text-sm">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                        <span>Generating your application...</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl md:text-5xl font-display font-bold">
              Powerful Features
            </h2>
            <p className="text-xl text-muted-foreground">
              Everything you need to build production-ready applications
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: <Sparkles className="w-6 h-6" />,
                title: "AI-Powered Prompts",
                description: "One-click prompt enhancement that transforms simple ideas into detailed specifications",
                gradient: "from-purple-500 to-pink-500"
              },
              {
                icon: <Code2 className="w-6 h-6" />,
                title: "Live Code Editor",
                description: "Professional Monaco editor with syntax highlighting and real-time preview",
                gradient: "from-blue-500 to-cyan-500"
              },
              {
                icon: <Zap className="w-6 h-6" />,
                title: "Instant Deployment",
                description: "One-click deployment to Vercel with automatic builds and custom domains",
                gradient: "from-yellow-500 to-orange-500"
              },
              {
                icon: <Shield className="w-6 h-6" />,
                title: "File Locking",
                description: "Protect critical files from AI modifications with granular control",
                gradient: "from-green-500 to-emerald-500"
              },
              {
                icon: <Cpu className="w-6 h-6" />,
                title: "Smart Context",
                description: "Intelligent token tracking prevents memory loss during long conversations",
                gradient: "from-red-500 to-rose-500"
              },
              {
                icon: <Rocket className="w-6 h-6" />,
                title: "Template Library",
                description: "8+ pre-built templates for SaaS, e-commerce, blogs, and more",
                gradient: "from-indigo-500 to-purple-500"
              },
            ].map((feature, i) => (
              <div key={i} className="group relative">
                <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl blur-xl"
                     style={{background: `linear-gradient(135deg, var(--tw-gradient-stops))`}} />
                <div className="relative glass rounded-2xl p-6 border border-white/20 hover:border-white/40 transition-all">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center text-white mb-4`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-display font-semibold mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground">
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Templates Section */}
      <section id="templates" className="py-20 px-6 bg-gradient-to-br from-purple-50/50 to-blue-50/50 dark:from-purple-950/20 dark:to-blue-950/20">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center space-y-4 mb-16">
            <h2 className="text-4xl md:text-5xl font-display font-bold">
              Start with Templates
            </h2>
            <p className="text-xl text-muted-foreground">
              Professional templates to kickstart your project
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { name: "SaaS Dashboard", category: "Dashboard", gradient: "from-blue-500 to-cyan-500" },
              { name: "E-commerce Store", category: "E-commerce", gradient: "from-purple-500 to-pink-500" },
              { name: "Landing Page", category: "Marketing", gradient: "from-yellow-500 to-orange-500" },
              { name: "Blog Platform", category: "Content", gradient: "from-green-500 to-emerald-500" },
              { name: "Portfolio", category: "Personal", gradient: "from-red-500 to-rose-500" },
              { name: "Admin Panel", category: "Dashboard", gradient: "from-indigo-500 to-purple-500" },
            ].map((template, i) => (
              <div key={i} className="group glass rounded-2xl overflow-hidden border border-white/20 hover:border-white/40 transition-all cursor-pointer">
                <div className={`h-32 bg-gradient-to-br ${template.gradient} flex items-center justify-center`}>
                  <Globe className="w-12 h-12 text-white opacity-50" />
                </div>
                <div className="p-6">
                  <div className="text-xs text-muted-foreground mb-1">{template.category}</div>
                  <h3 className="text-lg font-display font-semibold">{template.name}</h3>
                </div>
              </div>
            ))}
          </div>

          <div className="text-center mt-8">
            <Link href="/templates">
              <Button size="lg" variant="outline">
                View All Templates
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl">
          <div className="glass rounded-3xl p-12 md:p-16 text-center border-2 border-white/20 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10" />
            <div className="relative z-10 space-y-6">
              <h2 className="text-4xl md:text-5xl font-display font-bold">
                Ready to Build Something Amazing?
              </h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Join developers building the future with AI-powered development.
                Start creating your app today, completely free.
              </p>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
                <Link href="/signup">
                  <Button size="lg" className="gradient-primary text-white border-0 text-lg px-8 py-6 shine">
                    <Rocket className="w-5 h-5 mr-2" />
                    Get Started Free
                  </Button>
                </Link>
                <Link href="https://github.com" target="_blank">
                  <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                    <Github className="w-5 h-5 mr-2" />
                    View on GitHub
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-border">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="font-display font-bold">AI App Builder</span>
            </div>

            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <Link href="/docs" className="hover:text-foreground transition-colors">Documentation</Link>
              <Link href="/templates" className="hover:text-foreground transition-colors">Templates</Link>
              <Link href="/support" className="hover:text-foreground transition-colors">Support</Link>
              <Link href="/privacy" className="hover:text-foreground transition-colors">Privacy</Link>
            </div>

            <div className="text-sm text-muted-foreground">
              © 2024 AI App Builder. Built with ❤️ and AI.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
