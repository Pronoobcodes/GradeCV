import type { Metadata } from "next";
import { Plus_Jakarta_Sans, Playfair_Display } from "next/font/google";
import { cookies } from "next/headers";
import "./globals.css";

const plusJakartaSans = Plus_Jakarta_Sans({
  variable: "--font-plus-jakarta",
  subsets: ["latin"],
});

const playfairDisplay = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "CV Grader",
  description: "Grade your CV against any job description using AI.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies();
  const isAuthenticated = cookieStore.has("token");

  return (
    <html
      lang="en"
      className={`${plusJakartaSans.variable} ${playfairDisplay.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-background text-text-main font-sans" suppressHydrationWarning>
        {/* Navigation / Header Shell */}
        <header className="w-full border-b border-gray-200 bg-surface h-16 flex items-center px-6 shadow-sm">
          <div className="max-w-6xl mx-auto w-full flex justify-between items-center">
            <a href="/" className="text-xl font-serif font-bold text-primary hover:opacity-80 transition">CV Grader</a>
            <nav className="space-x-4">
              {isAuthenticated ? (
                <>
                  <a href="/grade" className="text-sm font-medium text-text-muted hover:text-text-main transition">Dashboard</a>
                  <form action="/api/auth/logout" method="POST" className="inline">
                    <button type="submit" className="text-sm font-medium bg-gray-100 text-text-main px-4 py-2 rounded-full hover:bg-gray-200 transition">
                      Log Out
                    </button>
                  </form>
                </>
              ) : (
                <>
                  <a href="/login" className="text-sm font-medium text-text-muted hover:text-text-main transition">Log In</a>
                  <a href="/register" className="text-sm font-medium bg-primary text-surface px-4 py-2 rounded-full hover:bg-gray-800 transition">Sign Up</a>
                </>
              )}
            </nav>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-grow w-full max-w-6xl mx-auto px-6 py-8 flex flex-col">
          {children}
        </main>

        {/* Footer Shell */}
        <footer className="w-full border-t border-gray-200 bg-surface py-6 mt-auto">
          <div className="max-w-6xl mx-auto px-6 text-center text-sm text-text-muted">
            &copy; {new Date().getFullYear()} CV Grader. All rights reserved.
          </div>
        </footer>
      </body>
    </html>
  );
}

