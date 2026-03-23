import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";
import AuthGuard from "@/components/AuthGuard";

export const metadata: Metadata = {
  title: "WealthArena Dashboard",
  description: "Read-only portfolio dashboard for WealthArena",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <AuthGuard>{children}</AuthGuard>
        </AuthProvider>
      </body>
    </html>
  );
}
