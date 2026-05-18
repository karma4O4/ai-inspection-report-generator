'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useStore } from '../../../lib/store';
import { Button } from '../../../components/ui/Button';
import { ImageUploader } from '../../../components/images/ImageUploader';
import { ImageCard } from '../../../components/images/ImageCard';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';
import { 
  ArrowLeft, Calendar, MapPin, User, FileText, Wand2, FileDown, 
  RefreshCw, CheckCircle, Save, Settings
} from 'lucide-react';
import Link from 'next/link';
import toast from 'react-hot-toast';

export default function ReportWorkspace() {
  const params = useParams();
  const router = useRouter();
  const id = params.id as string;

  const {
    currentReport,
    fetchReportDetails,
    isFetchingReportDetails,
    fetchCategories,
    generateConclusion,
    isGeneratingConclusion,
    generatePDF,
    isGeneratingPDF,
    updateReport
  } = useStore();

  const [conclusion, setConclusion] = useState("");
  const [hasUnsavedConclusion, setHasUnsavedConclusion] = useState(false);

  useEffect(() => {
    if (id) {
      fetchReportDetails(id);
      fetchCategories();
    }
  }, [id, fetchReportDetails, fetchCategories]);

  // Sync local conclusion state when currentReport updates
  useEffect(() => {
    if (currentReport) {
      setConclusion(currentReport.conclusion || "");
    }
  }, [currentReport]);

  if (isFetchingReportDetails) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#030712]">
        <LoadingSpinner />
      </div>
    );
  }

  if (!currentReport) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#030712] p-4 text-center">
        <h3 className="text-xl font-bold text-white mb-2">Workspace Not Found</h3>
        <p className="text-sm text-gray-400 mb-6">The report workspace you requested does not exist or has been deleted.</p>
        <Link href="/dashboard">
          <Button variant="primary">Return to Dashboard</Button>
        </Link>
      </div>
    );
  }

  const handleSaveConclusion = () => {
    updateReport(currentReport.id, { conclusion });
    setHasUnsavedConclusion(false);
  };

  const handleConclusionChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setConclusion(e.target.value);
    setHasUnsavedConclusion(true);
  };

  const handleAIConclusion = async () => {
    await generateConclusion(currentReport.id);
  };

  const handleGeneratePDF = async () => {
    await generatePDF(currentReport.id);
  };

  const handleDownloadPDF = () => {
    if (!currentReport.pdf_url) return;
    
    // Open in a new tab or trigger direct stream download
    const isLocalPath = !currentReport.pdf_url.startsWith('http');
    const downloadUrl = isLocalPath 
      ? `${process.env.NEXT_PUBLIC_API_URL}${currentReport.pdf_url}`
      : currentReport.pdf_url;
      
    window.open(downloadUrl, '_blank');
  };

  const statusColors = {
    draft: "bg-amber-950/60 text-amber-300 border-amber-800/80",
    completed: "bg-emerald-950/60 text-emerald-300 border-emerald-800/80"
  };

  return (
    <div className="min-h-screen bg-[#030712] flex flex-col pb-20">
      
      {/* Top Header Section */}
      <div className="border-b border-gray-800/40 pb-6 mb-8 flex flex-col gap-4">
        {/* Back Link */}
        <Link 
          href="/dashboard" 
          className="inline-flex items-center gap-1.5 text-xs font-bold text-gray-500 hover:text-white uppercase tracking-widest transition-colors"
        >
          <ArrowLeft size={14} />
          Back to Workspaces
        </Link>

        {/* Title row */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-extrabold text-white tracking-tight">
                {currentReport.report_title}
              </h1>
              <span className={`px-2.5 py-1 text-xs font-bold uppercase tracking-wider rounded-full border ${statusColors[currentReport.status]}`}>
                {currentReport.status}
              </span>
            </div>
            {/* Metadata row */}
            <div className="flex flex-wrap items-center gap-x-6 gap-y-2 mt-3 text-sm text-gray-400">
              <div className="flex items-center gap-1.5">
                <User size={14} className="text-blue-400" />
                <span><b>Client:</b> {currentReport.client_name}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <MapPin size={14} className="text-indigo-400" />
                <span><b>Site:</b> {currentReport.site_name}</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Calendar size={14} className="text-purple-400" />
                <span><b>Inspected:</b> {new Date(currentReport.inspection_date).toLocaleDateString(undefined, { dateStyle: 'medium' })}</span>
              </div>
            </div>
          </div>

          {/* Action trigger PDF */}
          <div className="flex gap-2.5 w-full md:w-auto">
            <Button
              onClick={handleGeneratePDF}
              isLoading={isGeneratingPDF}
              variant={currentReport.pdf_url ? "secondary" : "primary"}
              className="flex-1 md:flex-initial text-sm font-bold py-2.5"
            >
              <RefreshCw size={15} />
              {currentReport.pdf_url ? "Recompile PDF" : "Generate PDF"}
            </Button>
            
            {currentReport.pdf_url && (
              <Button
                onClick={handleDownloadPDF}
                variant="primary"
                className="flex-1 md:flex-initial text-sm font-bold py-2.5 shadow-blue-500/10"
              >
                <FileDown size={15} />
                Download PDF
              </Button>
            )}
          </div>
        </div>
      </div>

      {/* Grid container split layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* LEFT 2 COLUMNS: Photos & Upload */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h2 className="text-xl font-bold text-white">Photographic Evidence</h2>
            <p className="text-xs text-gray-400">Add inspection site photos and analyze them using AI descriptions & OCR.</p>
          </div>

          <ImageUploader reportId={currentReport.id} />

          {/* Photos list */}
          <div className="flex flex-col gap-5 mt-2">
            {!currentReport.images || currentReport.images.length === 0 ? (
              <div className="glass-panel text-center p-12 py-16 rounded-2xl border-gray-800/80">
                <p className="text-sm text-gray-500 font-semibold">No photos uploaded to this report yet.</p>
                <p className="text-xs text-gray-600 mt-1">Use the dropzone above to drag and drop inspection photos.</p>
              </div>
            ) : (
              currentReport.images.map((img) => (
                <ImageCard key={img.id} image={img} />
              ))
            )}
          </div>
        </div>

        {/* RIGHT COLUMN: Conclusion & Export */}
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <h2 className="text-xl font-bold text-white">Report Synthesis</h2>
            <p className="text-xs text-gray-400">Compile findings and write the executive summary.</p>
          </div>

          {/* Executive Summary Card */}
          <div className="glass-panel p-6 rounded-2xl border-gray-800/80 flex flex-col gap-4">
            <div className="flex justify-between items-center pb-3 border-b border-gray-800/40">
              <h3 className="text-sm font-extrabold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
                <FileText size={15} className="text-blue-400" />
                Executive Summary
              </h3>
            </div>

            <p className="text-xs text-gray-500 leading-relaxed">
              Consolidate all findings from the photographic evidence into a comprehensive conclusion.
            </p>

            <Button
              onClick={handleAIConclusion}
              isLoading={isGeneratingConclusion}
              disabled={!currentReport.images || currentReport.images.length === 0}
              variant="secondary"
              className="w-full text-xs font-bold border-indigo-900/40 text-indigo-300 bg-indigo-950/20 hover:bg-indigo-900/30 py-2.5 mt-1"
            >
              <Wand2 size={13} />
              Generate Summary (AI)
            </Button>

            <textarea
              value={conclusion}
              onChange={handleConclusionChange}
              placeholder="The conclusion or summary text goes here..."
              className="glass-input p-3.5 rounded-lg text-sm text-white w-full h-[220px] mt-2 resize-none leading-relaxed"
            />

            {hasUnsavedConclusion && (
              <Button
                onClick={handleSaveConclusion}
                variant="primary"
                className="w-full text-xs font-bold py-2 shadow-indigo-500/10"
              >
                <Save size={13} />
                Save Conclusion Updates
              </Button>
            )}
          </div>

          {/* Compilation Checklist panel */}
          <div className="glass-panel p-6 rounded-2xl border-gray-800/80 flex flex-col gap-4">
            <h3 className="text-sm font-extrabold text-gray-300 uppercase tracking-wider flex items-center gap-1.5 pb-3 border-b border-gray-800/40">
              <CheckCircle size={15} className="text-emerald-400" />
              Inspection Checklist
            </h3>

            <ul className="flex flex-col gap-3 mt-1">
              <li className="flex items-center gap-2.5 text-xs text-gray-400">
                <span className={`h-4.5 w-4.5 rounded-full flex items-center justify-center border text-[9px] font-bold ${
                  currentReport.images && currentReport.images.length > 0 
                    ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400' 
                    : 'border-gray-800 text-gray-600'
                }`}>
                  ✓
                </span>
                <span>Upload site photographs ({currentReport.images?.length || 0} uploaded)</span>
              </li>

              <li className="flex items-center gap-2.5 text-xs text-gray-400">
                <span className={`h-4.5 w-4.5 rounded-full flex items-center justify-center border text-[9px] font-bold ${
                  currentReport.images && currentReport.images.some(img => img.ai_description || img.edited_description)
                    ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400' 
                    : 'border-gray-800 text-gray-600'
                }`}>
                  ✓
                </span>
                <span>Analyze/Describe each photograph</span>
              </li>

              <li className="flex items-center gap-2.5 text-xs text-gray-400">
                <span className={`h-4.5 w-4.5 rounded-full flex items-center justify-center border text-[9px] font-bold ${
                  currentReport.conclusion 
                    ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400' 
                    : 'border-gray-800 text-gray-600'
                }`}>
                  ✓
                </span>
                <span>Generate Executive Summary</span>
              </li>

              <li className="flex items-center gap-2.5 text-xs text-gray-400">
                <span className={`h-4.5 w-4.5 rounded-full flex items-center justify-center border text-[9px] font-bold ${
                  currentReport.pdf_url
                    ? 'bg-emerald-950/60 border-emerald-800 text-emerald-400' 
                    : 'border-gray-800 text-gray-600'
                }`}>
                  ✓
                </span>
                <span>Generate and Verify PDF Report</span>
              </li>
            </ul>
          </div>

        </div>

      </div>

    </div>
  );
}
