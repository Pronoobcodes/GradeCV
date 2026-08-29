"use client"

import * as React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card"
import { Alert } from "@/components/ui/Alert"
import { ScoreGauge } from "@/components/ui/ScoreGauge"
import { Spinner } from "@/components/ui/Spinner"
import { fetchApi } from "@/lib/api"

export default function HistoryPage() {
  const [loading, setLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)
  const [results, setResults] = React.useState<any[]>([])

  React.useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchApi("/grading/")
        setResults(data)
      } catch (err: any) {
        setError(err.message || "Failed to load history.")
      } finally {
        setLoading(false)
      }
    }
    loadHistory()
  }, [])

  if (loading) {
    return (
      <div className="flex justify-center py-24">
        <Spinner className="w-8 h-8" />
      </div>
    )
  }

  if (error) {
    return <Alert variant="error" title="Error Loading History" description={error} />
  }

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-serif font-bold text-primary">Your History</h2>
          <p className="text-text-muted mt-2">Past CV grading results and feedback.</p>
        </div>
        <a href="/grade" className="text-sm font-medium text-primary-blue hover:underline">&larr; New Grade</a>
      </div>

      {results.length === 0 ? (
        <div className="text-center py-24 bg-gray-50 rounded-2xl border border-dashed border-gray-200">
          <p className="text-text-muted mb-4">You haven't graded any CVs yet.</p>
          <a href="/grade" className="text-primary-blue font-medium hover:underline">Grade your first CV</a>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {results.map((item) => (
            <Card key={item.id} className="overflow-hidden">
              <div className="flex flex-col md:flex-row">
                <div className="bg-gray-50 p-6 flex items-center justify-center border-b md:border-b-0 md:border-r border-gray-100 min-w-[200px]">
                  <ScoreGauge score={item.score} />
                </div>
                <div className="p-6 flex-1">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-semibold text-lg">Grading #{item.id}</h3>
                      <p className="text-sm text-text-muted">
                        {new Date(item.created_at).toLocaleDateString(undefined, { 
                          year: 'numeric', month: 'short', day: 'numeric', 
                          hour: '2-digit', minute: '2-digit' 
                        })}
                      </p>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <h4 className="font-semibold text-sm uppercase tracking-wider text-text-muted">Feedback Snippet</h4>
                    <p className="text-sm text-text-main line-clamp-3 leading-relaxed">
                      {item.feedback}
                    </p>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
