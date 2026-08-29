"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { FileUpload } from "@/components/ui/FileUpload"
import { Input, Textarea } from "@/components/ui/Input"
import { Button } from "@/components/ui/Button"
import { Alert } from "@/components/ui/Alert"
import { ScoreGauge } from "@/components/ui/ScoreGauge"
import { Badge } from "@/components/ui/Badge"
import { Spinner } from "@/components/ui/Spinner"
import { fetchApi } from "@/lib/api"

export default function GradePage() {
  const [file, setFile] = React.useState<File | null>(null)
  const [jobTitle, setJobTitle] = React.useState("")
  const [jobDescription, setJobDescription] = React.useState("")
  
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState<string | null>(null)
  const [result, setResult] = React.useState<any | null>(null)

  const handleGrade = async () => {
    if (!file) return setError("Please upload a CV PDF.")
    if (!jobTitle) return setError("Please enter a Job Title.")
    if (!jobDescription) return setError("Please enter the Job Description.")

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // 1. Create Job Description
      const jdRes = await fetchApi("/job-descriptions/", {
        method: "POST",
        body: JSON.stringify({ title: jobTitle, content: jobDescription })
      })
      
      // 2. Upload CV
      const formData = new FormData()
      formData.append("file", file)
      
      const cvRes = await fetchApi("/cvs/", {
        method: "POST",
        body: formData,
        // Don't set content-type for FormData, fetch automatically sets it with the correct boundary
        headers: {} 
      })

      // 3. Grade
      const gradeRes = await fetchApi("/grading/", {
        method: "POST",
        body: JSON.stringify({ cv_id: cvRes.id, job_description_id: jdRes.id })
      })

      setResult(gradeRes)
    } catch (err: any) {
      setError(err.message || "An error occurred during grading.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-serif font-bold text-primary">Grade Your CV</h2>
          <p className="text-text-muted mt-2">Upload your resume and paste the job description to get instant AI-powered feedback.</p>
        </div>
        <a href="/history" className="text-sm font-medium text-primary-blue hover:underline">View History &rarr;</a>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Left Column: Form */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>1. Upload CV</CardTitle>
            </CardHeader>
            <CardContent>
              <FileUpload onFileSelect={setFile} selectedFile={file} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>2. Job Description</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Job Title</label>
                <Input 
                  placeholder="e.g. Senior Frontend Engineer" 
                  value={jobTitle}
                  onChange={(e) => setJobTitle(e.target.value)}
                  disabled={loading}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Job Requirements</label>
                <Textarea 
                  placeholder="Paste the full job description here..."
                  className="min-h-[200px]"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  disabled={loading}
                />
              </div>
            </CardContent>
          </Card>

          {error && <Alert variant="error" title="Grading Error" description={error} />}

          <Button 
            size="lg" 
            className="w-full" 
            onClick={handleGrade} 
            disabled={loading || !file || !jobTitle || !jobDescription}
          >
            {loading ? (
              <>
                <Spinner className="mr-2 text-surface" /> Analyzing Match...
              </>
            ) : "Analyze CV Match"}
          </Button>
        </div>

        {/* Right Column: Results */}
        <div>
          {loading && (
            <div className="h-full flex flex-col items-center justify-center text-center p-12 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
              <Spinner className="w-12 h-12 mb-4 text-primary-blue" />
              <h3 className="text-lg font-semibold">AI is analyzing your CV...</h3>
              <p className="text-sm text-text-muted mt-2">This may take a few moments as we cross-reference your experience.</p>
            </div>
          )}

          {!loading && !result && (
            <div className="h-full flex items-center justify-center text-center p-12 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
              <p className="text-text-muted">Submit your CV and job description to see your results here.</p>
            </div>
          )}

          {!loading && result && (
            <Card className="h-full bg-gradient-to-b from-surface to-gray-50">
              <CardHeader className="text-center pb-0">
                <CardTitle>Match Score</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col items-center pt-6 space-y-8">
                <ScoreGauge score={result.score} className="scale-125" />
                
                <div className="w-full space-y-6 mt-8">
                  <div className="space-y-3 pt-4 border-t border-gray-200">
                    <h4 className="font-semibold text-sm uppercase tracking-wider text-text-muted">Feedback</h4>
                    <p className="text-sm leading-relaxed text-text-main whitespace-pre-line">
                      {result.feedback}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
