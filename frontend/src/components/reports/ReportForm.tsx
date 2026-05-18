'use client';

import React, { useState } from 'react';
import { useStore } from '../../lib/store';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

interface ReportFormProps {
  onClose?: () => void;
}

export const ReportForm: React.FC<ReportFormProps> = ({ onClose }) => {
  const createReport = useStore((state) => state.createReport);
  const isSubmitting = useStore((state) => state.isSubmittingReport);
  const router = useRouter();
  
  const [title, setTitle] = useState('');
  const [client, setClient] = useState('');
  const [site, setSite] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || !client || !site || !date) {
      toast.error("Please fill in all required fields.");
      return;
    }

    const payload = {
      report_title: title,
      client_name: client,
      site_name: site,
      inspection_date: date,
      status: "draft" as const
    };

    const newReport = await createReport(payload);
    if (newReport) {
      if (onClose) onClose();
      // Redirect straight to report workspace!
      router.push(`/reports/${newReport.id}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-5 w-full">
      <Input
        id="title"
        label="Report Title"
        placeholder="e.g. Commercial Roof & Eaves Inspection"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />

      <Input
        id="client"
        label="Client Name"
        placeholder="e.g. Apex Property Ventures"
        value={client}
        onChange={(e) => setClient(e.target.value)}
        required
      />

      <Input
        id="site"
        label="Site Location / Address"
        placeholder="e.g. 102 West Boulevard, Building C"
        value={site}
        onChange={(e) => setSite(e.target.value)}
        required
      />

      <Input
        id="date"
        label="Date of Inspection"
        type="date"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        required
      />

      <div className="flex gap-3 justify-end mt-4">
        {onClose && (
          <Button type="button" variant="secondary" onClick={onClose}>
            Cancel
          </Button>
        )}
        <Button type="submit" variant="primary" isLoading={isSubmitting}>
          Create Workspace
        </Button>
      </div>
    </form>
  );
};
