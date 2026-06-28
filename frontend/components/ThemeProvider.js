"use client";
/**
 * ThemeProvider for AI-Kavach SIEM Console
 * --------------------------------------------------------
 * Wrap your root layout's children with this component.
 * Works together with the inline script in layout.js that prevents
 * a flash-of-wrong-theme on first paint.
 *
 * TAILWIND V4 NOTE: dark mode is driven purely by the "dark" class on
 * <html>. globals.css defines :root (light) and .dark (dark) variable
 * sets — no tailwind.config.js flag needed in v4.
 */
import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext({
  theme: "dark",
  toggleTheme: () => {},
});

const STORAGE_KEY = "ai-kavach-theme";

export function ThemeProvider({ children }) {
  // Read the class the inline script (in layout.js <head>) already set
  // on <html> before this component ever mounts — so initial state matches
  // what's already on screen, with zero flash.
  const [theme, setTheme] = useState(() => {
    if (typeof document === "undefined") return "dark"; // SSR fallback
    return document.documentElement.classList.contains("dark") ? "dark" : "light";
  });

  useEffect(() => {
    const root = document.documentElement;
    if (theme === "dark") {
      root.classList.add("dark");
    } else {
      root.classList.remove("dark");
    }
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  function toggleTheme() {
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));
  }

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
