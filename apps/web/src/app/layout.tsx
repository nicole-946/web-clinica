import type { ReactNode } from "react";
import { SessionBanner } from "@/components/SessionBanner";
import "./globals.css";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body>
        <SessionBanner />
        <main className="min-h-screen">{children}</main>
      </body>
    </html>
  );
}
