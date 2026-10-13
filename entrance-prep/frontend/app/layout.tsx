import type { Metadata, Viewport } from "next";
import "./globals.css";
import "katex/dist/katex.min.css";
export const metadata: Metadata = {
  title: "Entrance Prep | Mechanical Engineering @ RUPP",
  description:
    "Practise Mathematics, Physics and Logic for the Mechanical Engineering entrance examination, with a worked explanation behind every answer.",
  manifest: "/manifest.webmanifest",
  // me-icon, not me-logo: the logo is 501x361, and a favicon is drawn into a
  // square box, so the browser squashed it by about 28%. me-icon is the same
  // mark padded onto a square canvas, so its proportions survive.
  icons: { icon: "/brand/me-icon.png", apple: "/brand/me-icon.png" },
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
