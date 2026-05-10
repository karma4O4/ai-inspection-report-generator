import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/components/auth/AuthProvider";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Property Inspection Report Generator",
  description: "Generate professional, high-fidelity engineering and building inspection reports from site photos with GPT-4 Vision & OCR.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <AuthProvider>
          <Toaster 
            position="top-right" 
            toastOptions={{
              style: {
                background: '#111827',
                color: '#fff',
                border: '1px solid #1f2937',
              },
            }}
          />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
