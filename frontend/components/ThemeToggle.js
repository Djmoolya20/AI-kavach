"use client";

import { useState, useEffect } from "react";
import { Sun, Moon } from "lucide-react";
import { useTheme } from "./ThemeProvider";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  // Prevent hydration mismatch — only render icon after client mount
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);

  if (!mounted) {
    return (
      <button
        className="inline-flex items-center justify-center h-9 w-9 rounded-lg border border-panel-border bg-panel"
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
          : "border-slate-300 bg-white text-slate-600 hover:bg-slate-100 hover:text-slate-900 shadow-sm"
        }
      `}
    >
      {isDark
        ? <Sun  className="h-4 w-4" strokeWidth={2} />
        : <Moon className="h-4 w-4" strokeWidth={2} />
      }
    </button>
  );
}
