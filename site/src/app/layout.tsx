import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const SITE_URL = "https://tools-for-thinking.netlify.app";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Dennett's Thinking Tools",
    template: "%s — Dennett's Thinking Tools",
  },
  description:
    "A comprehensive collection of 77 intuition pumps and tools for thinking from Daniel C. Dennett's \"Intuition Pumps and Other Tools for Thinking\".",
  keywords: [
    "Daniel Dennett",
    "intuition pumps",
    "thinking tools",
    "tools for thinking",
    "critical thinking",
    "philosophy",
    "reasoning",
    "mental models",
  ],
  authors: [{ name: "Ashutosh Sanzgiri" }],
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    siteName: "Dennett's Thinking Tools",
    url: SITE_URL,
    title: "Dennett's Thinking Tools",
    description:
      "77 intuition pumps and tools for thinking from Daniel C. Dennett, with practical exercises for each.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Dennett's Thinking Tools",
    description:
      "77 intuition pumps and tools for thinking from Daniel C. Dennett, with practical exercises for each.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
