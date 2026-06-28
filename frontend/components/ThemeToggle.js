"use client";

import { useState, useEffect } from "react";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "./ThemeProvider";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  // FIX: prevent hydration mismatch.
  // On the server, theme is unknown. We only render the icon after the
  // component mounts on the client so server and client HTML always match.
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  if (!mounted) {
    // Render a blank placeholder with the same dimensions so layout doesn't shift
    return (
      <button
        className="inline-flex items-center justify-center h-9 w-9 rounded-lg border border-slate-700 bg-slate-800"
        aria-label="Toggle theme"
        disabled
      />
    );
  }

  const isDark = theme === "dark";

  return (
    <button
      onClick={toggleTheme}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      title={isDark ? "Switch to light mode" : "Switch to dark mode"}
      className={`
        inline-flex items-center justify-center
        h-9 w-9 rounded-lg
        border transition-colors duration-200
        ${isDark
          ? "border-slate-700 bg-slate-800 text-slate-300 hover:bg-slate-700 hover:text-white"
          : "border-slate-300 bg-white text-slate-600 hover:bg-slate-100 hover:text-slate-900"
        }
      `}
    >
      {isDark ? (
        <Sun  className="h-4 w-4" strokeWidth={2} />
      ) : (
        <Moon className="h-4 w-4" strokeWidth={2} />
      )}
    </button>
  );
}