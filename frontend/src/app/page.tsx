import { Button } from "@/components/ui/Button";
import Link from "next/link";
import { ArrowRight, CheckCircle2 } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center animate-in fade-in duration-700">
      
      {/* Hero Section */}
      <section className="w-full py-20 md:py-32 flex flex-col items-center text-center px-6">
        <div className="inline-flex items-center rounded-full border border-gray-200 bg-surface px-3 py-1 text-sm font-medium mb-8 text-primary-blue shadow-sm">
          <span className="flex h-2 w-2 rounded-full bg-primary-blue mr-2"></span>
          Now powered by AI
        </div>
        
        <h1 className="text-5xl md:text-7xl font-serif font-bold text-primary max-w-4xl tracking-tight leading-tight">
          Grade your CV against <br className="hidden md:block"/> any job description.
        </h1>
        
        <p className="mt-6 text-xl text-text-muted max-w-2xl leading-relaxed">
          Upload your resume, paste the job requirements, and get instant, AI-driven feedback on how perfectly you match the role.
        </p>
        
        <div className="mt-10 flex flex-col sm:flex-row gap-4">
          <Link href="/register">
            <Button size="lg" className="w-full sm:w-auto h-14 px-8 text-lg flex items-center group">
              Get Started for Free
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </Link>
          <Link href="/login">
            <Button size="lg" variant="outline" className="w-full sm:w-auto h-14 px-8 text-lg">
              Sign In
            </Button>
          </Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="w-full py-20 mt-12">
        <div className="max-w-5xl mx-auto px-6 md:px-0">
          <h2 className="text-3xl font-serif font-bold text-center text-primary mb-16">
            How it works
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-x-12 gap-y-10 text-center md:text-left">
            <div className="flex flex-col items-center md:items-start">
              <div className="w-12 h-12 rounded-2xl bg-[#E0E7FF] text-primary-blue flex items-center justify-center mb-6 shadow-sm">
                <span className="text-xl font-bold font-serif">1</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Upload your CV</h3>
              <p className="text-text-muted leading-relaxed">
                Drag and drop your latest PDF resume into our secure, private system.
              </p>
            </div>
            
            <div className="flex flex-col items-center md:items-start">
              <div className="w-12 h-12 rounded-2xl bg-[#E0E7FF] text-primary-blue flex items-center justify-center mb-6 shadow-sm">
                <span className="text-xl font-bold font-serif">2</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Paste the Job</h3>
              <p className="text-text-muted leading-relaxed">
                Found your dream role? Paste the requirements so our AI knows exactly what to look for.
              </p>
            </div>
            
            <div className="flex flex-col items-center md:items-start">
              <div className="w-12 h-12 rounded-2xl bg-[#E0E7FF] text-primary-blue flex items-center justify-center mb-6 shadow-sm">
                <span className="text-xl font-bold font-serif">3</span>
              </div>
              <h3 className="text-xl font-bold mb-3">Get Graded</h3>
              <p className="text-text-muted leading-relaxed">
                Instantly receive a match score and personalized feedback on how to improve your chances.
              </p>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
