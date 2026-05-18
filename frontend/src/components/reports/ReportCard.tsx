import React from 'react';
import { Report } from '../../types';
import Link from 'next/link';
import { format } from 'date-fns';
import { Calendar, MapPin, User, FileText, Trash2, ArrowRight } from 'lucide-react';
import { useStore } from '../../lib/store';

interface ReportCardProps {
  report: Report;
}

export const ReportCard: React.FC<ReportCardProps> = ({ report }) => {
  const deleteReport = useStore((state) => state.deleteReport);

  const handleDelete = (e: React.MouseEvent) => {
    e.preventDefault();
    if (window.confirm(`Are you sure you want to delete the report for "${report.report_title}"?`)) {
      deleteReport(report.id);
    }
  };

  const statusColors = {
    draft: "bg-amber-950/60 text-amber-300 border-amber-800/80",
    completed: "bg-emerald-950/60 text-emerald-300 border-emerald-800/80"
  };

  return (
    <div className="glass-card rounded-xl p-6 flex flex-col justify-between h-full transition-all hover:translate-y-[-2px]">
      <div>
        <div className="flex justify-between items-start mb-4">
          <span className={`px-2.5 py-1 text-xs font-bold uppercase tracking-wider rounded-full border ${statusColors[report.status || 'draft']}`}>
            {report.status || 'draft'}
          </span>
          <button
            onClick={handleDelete}
            className="text-gray-500 hover:text-red-400 p-1.5 rounded-lg hover:bg-red-950/30 transition-colors"
            title="Delete Report"
          >
            <Trash2 size={16} />
          </button>
        </div>

        <h3 className="text-xl font-extrabold text-white mb-3 line-clamp-1">
          {report.report_title}
        </h3>

        <div className="flex flex-col gap-2 mb-6">
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <User size={14} className="text-blue-400" />
            <span className="line-clamp-1"><b>Client:</b> {report.client_name}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <MapPin size={14} className="text-indigo-400" />
            <span className="line-clamp-1"><b>Site:</b> {report.site_name}</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <Calendar size={14} className="text-purple-400" />
            <span><b>Date:</b> {format(new Date(report.inspection_date), 'MMM dd, yyyy')}</span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between pt-4 border-t border-gray-800/60 mt-auto">
        <span className="text-xs text-gray-500 font-medium">
          {report.images?.length || 0} Photos Uploaded
        </span>
        
        <Link
          href={`/reports/${report.id}`}
          className="inline-flex items-center gap-1.5 text-sm font-bold text-blue-400 hover:text-blue-300 hover:underline transition-colors"
        >
          Open Editor
          <ArrowRight size={14} />
        </Link>
      </div>
    </div>
  );
};
