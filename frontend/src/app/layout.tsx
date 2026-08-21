import type { Metadata } from "next";
import OpenHouseWidget from "@/components/OpenHouseWidget";
import { getAnnouncedEvent } from "@/lib/api";
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

export default async function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  // Fetched here because the card sits outside every page. The collection is
  // cached, so this costs one request a minute across the whole site rather
  // than one per page.
  const announced = await getAnnouncedEvent();

  return (
    <html lang="en">
      <body>
        {children}
        <OpenHouseWidget event={announced} />
      </body>
    </html>
  );
}
