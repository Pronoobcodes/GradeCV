"use client"

import * as React from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/Button"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/Card"
import { Input } from "@/components/ui/Input"
import { Alert } from "@/components/ui/Alert"
import { Spinner } from "@/components/ui/Spinner"

export default function RegisterPage() {
  const router = useRouter()
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const formData = new FormData(e.currentTarget)
    const full_name = formData.get("name") as string
    const email = formData.get("email") as string
    const password = formData.get("password") as string

    try {
      // 1. Register the user
      const registerRes = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, full_name }),
      })
      
      const registerData = await registerRes.json()
      
      if (!registerRes.ok) {
        throw new Error(registerData.error || "Failed to register")
      }
      
      // 2. Automatically log them in
      const loginRes = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: email, password }),
      })
      
      if (!loginRes.ok) {
        throw new Error("Registered successfully, but auto-login failed. Please log in manually.")
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
          <CardTitle className="text-center text-3xl">Create Account</CardTitle>
          <p className="text-center text-text-muted text-sm mt-2">Sign up to get started with CV Grader</p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <Alert variant="error" title="Registration Failed" description={error} />}
            
            <div className="space-y-2">
              <label className="text-sm font-medium">Full Name</label>
              <Input 
                name="name" 
                type="text" 
                placeholder="John Doe" 
                required 
                disabled={loading} 
              />
            </div>

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
                minLength={6}
              />
            </div>
            
            <Button type="submit" className="w-full mt-4" disabled={loading} size="lg">
              {loading ? <Spinner className="text-surface" /> : "Sign Up"}
            </Button>
          </form>
        </CardContent>
        <CardFooter className="flex justify-center border-t border-gray-100 pt-6">
          <p className="text-sm text-text-muted">
            Already have an account? <a href="/login" className="text-primary-blue hover:underline font-medium">Log in</a>
          </p>
        </CardFooter>
      </Card>
    </div>
  )
}
