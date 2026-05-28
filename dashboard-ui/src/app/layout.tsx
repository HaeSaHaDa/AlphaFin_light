import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AlphaFin LTE Dashboard",
  description: "Financial AI Engine visualization dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko" className="dark">
      <body className="min-h-screen bg-background text-foreground antialiased">
        <div className="dashboard-root">{children}</div>
      </body>
    </html>
  );
}
