import * as React from "react"
import { UploadCloud } from "lucide-react"
import { cn } from "@/lib/utils"

interface FileUploadProps extends React.InputHTMLAttributes<HTMLInputElement> {
  onFileSelect: (file: File | null) => void;
  selectedFile: File | null;
}

export function FileUpload({ onFileSelect, selectedFile, className, ...props }: FileUploadProps) {
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      className={cn(
        "relative flex flex-col items-center justify-center w-full h-48 border-2 border-dashed border-gray-300 rounded-2xl bg-surface hover:bg-gray-50 transition-colors cursor-pointer",
        className
      )}
    >
      <input
        type="file"
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        onChange={handleChange}
        accept=".pdf"
        {...props}
      />
      <div className="flex flex-col items-center justify-center pt-5 pb-6 text-center px-4">
        <UploadCloud className="w-10 h-10 mb-3 text-primary-blue" />
        {selectedFile ? (
          <p className="mb-2 text-sm text-text-main font-semibold">
            {selectedFile.name}
          </p>
        ) : (
          <>
            <p className="mb-2 text-sm text-text-main">
              <span className="font-semibold">Click to upload</span> or drag and drop
            </p>
            <p className="text-xs text-text-muted">PDF (MAX. 10MB)</p>
          </>
        )}
      </div>
    </div>
  )
}
