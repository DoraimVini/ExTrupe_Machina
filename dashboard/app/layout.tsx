import type { Metadata } from "next";
import { Outfit } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
});

export const metadata: Metadata = {
  title: "Trupe BR | Dashboard de Gestão",
  description: "Sistema integrado de gestão para Trupe BR - Knitwear & Artesanato",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR" className={`${outfit.variable} antialiased`}>
      <body className="font-sans">
        {children}
      </body>
    </html>
  );
}
