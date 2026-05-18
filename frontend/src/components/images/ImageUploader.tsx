'use client';

import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, Image as ImageIcon } from 'lucide-react';
import { useStore } from '../../lib/store';
import toast from 'react-hot-toast';

interface ImageUploaderProps {
  reportId: string;
}

export const ImageUploader: React.FC<ImageUploaderProps> = ({ reportId }) => {
  const uploadImage = useStore((state) => state.uploadImage);
  const isUploading = useStore((state) => state.isUploadingImage);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    
    // Upload files sequentially or concurrently
    const uploadPromises = acceptedFiles.map(async (file) => {
      // Validate file extension manually as extra layer
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (ext !== 'png' && ext !== 'jpg' && ext !== 'jpeg') {
        toast.error(`${file.name} is not a supported format. Please upload PNG, JPG, or JPEG only.`);
        return;
      }
      // Validate size (5MB)
      if (file.size > 5 * 1024 * 1024) {
        toast.error(`${file.name} exceeds 5MB size limit.`);
        return;
      }
      await uploadImage(file, reportId);
    });

    await Promise.all(uploadPromises);
  }, [uploadImage, reportId]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg']
    },
    disabled: isUploading,
    multiple: true
  });

  return (
    <div
      {...getRootProps()}
      className={`glass-panel border-2 border-dashed rounded-2xl p-8 py-10 text-center cursor-pointer transition-all duration-300 flex flex-col items-center justify-center gap-3 ${
        isDragActive 
          ? 'border-blue-500 bg-blue-950/10' 
          : 'border-gray-800 hover:border-gray-700/80'
      } ${isUploading ? 'opacity-50 pointer-events-none' : ''}`}
    >
      <input {...getInputProps()} />
      
      <div className={`h-12 w-12 rounded-xl flex items-center justify-center text-blue-400 mb-2 shadow-inner ${
        isDragActive ? 'bg-blue-950 text-blue-300' : 'bg-gray-900/60 border border-gray-800'
      }`}>
        <UploadCloud size={24} />
      </div>
      
      <h3 className="text-base font-bold text-white">
        {isDragActive ? "Drop your photos here" : "Upload Inspection Photos"}
      </h3>
      
      <p className="text-xs text-gray-400 max-w-xs leading-relaxed">
        Drag and drop your roof, gutter, or defect photos here, or click to browse files. Supports PNG, JPG, JPEG (Max 5MB each).
      </p>

      {isUploading && (
        <div className="flex items-center gap-2 mt-2 px-3 py-1.5 rounded-full bg-blue-950/40 border border-blue-900/40 text-blue-400 text-xs font-bold animate-pulse">
          <svg className="animate-spin h-3.5 w-3.5 text-current" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
          Syncing media nodes...
        </div>
      )}
    </div>
  );
};
