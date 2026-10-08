import type { Metadata, Viewport } from "next";
import "./globals.css";
import "katex/dist/katex.min.css";
export const metadata: Metadata = {
  title: "Entrance Prep | Mechanical Engineering @ RUPP",
  description:
    "Practise the reasoning and mathematics the entrance exam asks for, with a worked explanation behind every answer.",
  manifest: "/manifest.webmanifest",
  icons: { icon: "/brand/me-logo.png", apple: "/brand/me-logo.png" },
};
export const viewport: Viewport = {
  themeColor: "#0B2D4D",
  width: "device-width",
  initialScale: 1,
};
export default function Layout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
