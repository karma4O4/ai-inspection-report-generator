'use client';

import React, { useEffect, useState } from 'react';
import { useStore } from '../../lib/store';
import { Button } from '@/components/ui/Button';
import { ReportCard } from '@/components/reports/ReportCard';
import { ReportForm } from '@/components/reports/ReportForm';
import { Plus, FolderOpen, FileText } from 'lucide-react';

export default function Dashboard() {
  const { reports, fetchReports, isFetchingReports } = useStore();
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchReports();
  }, [fetchReports]);

  return (
    <div className="flex flex-col gap-8">
      {/* Upper action row */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-gray-800/40 pb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Inspection Workspaces
          </h1>
          <p className="text-sm text-gray-400 mt-1">
            Create or edit active building inspection reports
          </p>
        </div>

        <Button
          onClick={() => setShowModal(true)}
          variant="primary"
          className="flex items-center gap-2"
        >
          <Plus size={18} />
          Create New Report
        </Button>
      </div>

      {/* Grid List */}
      {isFetchingReports ? (
        <div className="flex flex-col items-center justify-center py-20 gap-3">
          <svg className="animate-spin h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          <span className="text-sm text-gray-400 font-semibold animate-pulse-slow">Syncing report history...</span>
        </div>
      ) : reports.length === 0 ? (
        <div className="glass-panel flex flex-col items-center justify-center p-12 py-20 rounded-2xl border-dashed border-gray-800/80 text-center max-w-xl mx-auto mt-6">
          <div className="h-14 w-14 rounded-2xl bg-blue-950/40 border border-blue-800/40 flex items-center justify-center text-blue-400 mb-5">
            <FolderOpen size={28} />
          </div>
          <h3 className="text-xl font-bold text-white mb-2">No Reports Registered</h3>
          <p className="text-sm text-gray-400 mb-6 max-w-sm">
            Ready to generate your first professional PDF inspection report? Create a new report workspace to upload photos.
          </p>
          <Button onClick={() => setShowModal(true)} variant="primary">
            Create First Report
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {reports.map((report) => (
            <ReportCard key={report.id} report={report} />
          ))}
        </div>
      )}

      {/* Modal Dialog */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fadeIn">
          <div className="glass-panel max-w-lg w-full p-6 sm:p-8 rounded-2xl border-gray-800 shadow-2xl relative">
            <button 
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white p-1 rounded-lg"
            >
              ✕
            </button>
            <div className="mb-6">
              <h2 className="text-2xl font-extrabold text-white tracking-tight">
                New Inspection Report
              </h2>
              <p className="text-xs text-gray-400 mt-1">
                Establish the site details and client contact parameters.
              </p>
            </div>
            <ReportForm onClose={() => setShowModal(false)} />
          </div>
        </div>
      )}
    </div>
  );
}
