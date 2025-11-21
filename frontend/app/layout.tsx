import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const plusJakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-plus-jakarta",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AI App Builder - Build Apps with Natural Language",
  description: "Transform your ideas into production-ready web applications using AI. Build with natural language prompts, powered by Claude AI.",
  keywords: "AI, app builder, web development, Claude AI, no-code, low-code",
  authors: [{ name: "AI App Builder Team" }],
  openGraph: {
    title: "AI App Builder",
    description: "Build web applications with natural language prompts",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning className={`${inter.variable} ${plusJakarta.variable}`}>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
