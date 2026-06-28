import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "AI-Kavach | SIEM Console",
  description: "Real-time AI security proxy and SIEM dashboard",
  icons: {
    icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%232563eb'><path d='M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z'/></svg>",
  },
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
      suppressHydrationWarning
    >
      <head>
        {/*
          Runs before React hydrates or anything paints. Reads the saved
          theme (or falls back to system preference) and sets the "dark"
          class immediately - this is what ThemeProvider.jsx reads on
          mount, so there's no flash between "wrong default" and "correct
          saved theme."
        */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              (function () {
                try {
                  var saved = localStorage.getItem("ai-kavach-theme");
                  var isDark =
                    saved === "dark" ||
                    (saved !== "light" &&
                      !window.matchMedia("(prefers-color-scheme: light)").matches);
                  if (isDark) {
                    document.documentElement.classList.add("dark");
                  }
                } catch (e) {
                  document.documentElement.classList.add("dark");
                }
              })();
            `,
          }}
        />
      </head>
      <body className="min-h-full flex flex-col">
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  );
}