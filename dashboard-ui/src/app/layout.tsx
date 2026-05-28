import type { Metadata } from "next";
import "./globals.css";
import { AppProviders } from "./providers";
import { RuntimeShellLayout } from "@/layout/runtime-shell/RuntimeShellLayout";

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
        <AppProviders>
          <div className="dashboard-root">
            <RuntimeShellLayout>{children}</RuntimeShellLayout>
          </div>
        </AppProviders>
      </body>
    </html>
  );
}
