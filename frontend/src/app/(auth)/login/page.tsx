"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/Card"
import { Input } from "@/components/ui/Input"
import { Alert } from "@/components/ui/Alert"
import { Spinner } from "@/components/ui/Spinner"

export default function LoginPage() {
  const router = useRouter()
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const formData = new FormData(e.currentTarget)
    const username = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      })
      
      const data = await res.json()
      
      if (!res.ok) {
        throw new Error(data.error || "Failed to login")
      }
      
      // Navigate to dashboard
      router.push("/grade")
      router.refresh()
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex justify-center items-center h-[calc(100vh-200px)]">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center text-3xl">Welcome Back</CardTitle>
          <p className="text-center text-text-muted text-sm mt-2">Log in to continue to CV Grader</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <Alert variant="error" title="Login Failed" description={error} />}
            
            <div className="space-y-2">
              <label className="text-sm font-medium">Email Address</label>
              <Input 
                name="email" 
                type="email" 
                placeholder="name@example.com" 
                required 
                disabled={loading} 
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium">Password</label>
              <Input 
                name="password" 
                type="password" 
                placeholder="••••••••" 
                required 
                disabled={loading} 
              />
            </div>
            
            <Button type="submit" className="w-full mt-4" disabled={loading} size="lg">
              {loading ? <Spinner className="text-surface" /> : "Sign In"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center border-t border-gray-100 pt-6">
          <p className="text-sm text-text-muted">
            Don't have an account? <a href="/register" className="text-primary-blue hover:underline font-medium">Sign up</a>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}
