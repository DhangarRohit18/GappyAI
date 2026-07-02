import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata: Metadata = {
  title: "OrbitOS — The Autonomous Operating System for Startups",
  description:
    "One AI Employee. Infinite Productivity. OrbitOS autonomously manages your entire startup operations through 8 specialized AI agents powered by the Lemma SDK.",
  keywords: [
    "AI startup", "autonomous agents", "startup operations", "Lemma SDK",
    "AI COO", "project management AI", "multi-agent system"
  ],
  openGraph: {
    title: "OrbitOS — Autonomous AI Startup OS",
    description: "One AI Employee. Infinite Productivity.",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "OrbitOS — Autonomous AI Startup OS",
    description: "One AI Employee. Infinite Productivity.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
