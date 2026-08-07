import type { Metadata } from "next";
import OpenHouseWidget from "@/components/OpenHouseWidget";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mechanical Engineering Program | RUPP",
  description:
    "Study Mechanical Engineering at the Royal University of Phnom Penh: four focus areas, applied research, industry collaboration, and balanced theory and practice.",
  icons: {
    icon: [{ url: "/assets/me-favicon.png", type: "image/png" }],
    shortcut: ["/assets/me-favicon.png"],
    apple: [{ url: "/assets/me-favicon.png", type: "image/png" }],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        {children}
        <OpenHouseWidget />
      </body>
    </html>
  );
}
