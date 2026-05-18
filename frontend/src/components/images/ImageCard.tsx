'use client';

import React, { useState, useEffect } from 'react';
import { Image, Category } from '../../types';
import { useStore } from '../../lib/store';
import { Button } from '../ui/Button';
import { Eye, Wand2, ScanText, Trash2, Save, Layers } from 'lucide-react';

interface ImageCardProps {
  image: Image;
}

export const ImageCard: React.FC<ImageCardProps> = ({ image }) => {
  const { 
    categories, 
    updateImageMetadata, 
    deleteImage, 
    generateDescription, 
    runOCR,
    isGeneratingDescription,
    isRunningOCR
  } = useStore();

  const [category, setCategory] = useState(image.category || "General Maintenance");
  const [description, setDescription] = useState(image.edited_description || image.ai_description || "");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

  const isGenerating = isGeneratingDescription[image.id] || false;
  const isOCRRunning = isRunningOCR[image.id] || false;

  // Sync state if image values change from store updates (e.g. after AI generation)
  useEffect(() => {
    setDescription(image.edited_description || image.ai_description || "");
    if (image.category) {
      setCategory(image.category);
    }
  }, [image.edited_description, image.ai_description, image.category]);

  const handleSave = () => {
    updateImageMetadata(image.id, {
      category,
      edited_description: description
    });
    setHasUnsavedChanges(false);
  };

  const handleDescChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setDescription(e.target.value);
    setHasUnsavedChanges(true);
  };

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setCategory(val);
    updateImageMetadata(image.id, { category: val });
  };

  const handleAIDescribe = async () => {
    await generateDescription(image.id, category);
  };

  const handleOCR = async () => {
    await runOCR(image.id);
  };

  return (
    <div className="glass-panel rounded-xl overflow-hidden border-gray-800/80 hover:border-gray-700/60 transition-all flex flex-col lg:flex-row gap-6 p-5">
      
      {/* 1. Left side: Image and details */}
      <div className="flex-shrink-0 flex flex-col gap-3 lg:w-[260px] w-full">
        <div className="relative rounded-lg overflow-hidden border border-gray-800/80 bg-gray-950 aspect-video lg:aspect-[4/3] flex items-center justify-center">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={image.image_url.startsWith('http') ? image.image_url : `${process.env.NEXT_PUBLIC_API_URL}${image.image_url}`}
            alt={image.filename}
            className="object-cover w-full h-full"
          />
        </div>
        <div className="flex flex-col gap-1">
          <span className="text-xs font-bold text-gray-500 truncate max-w-[260px]">
            FILE: {image.filename}
          </span>
          <span className="text-xs text-gray-600">
            Uploaded {new Date(image.created_at).toLocaleTimeString()}
          </span>
        </div>

        {/* Delete Trigger */}
        <Button
          onClick={() => deleteImage(image.id)}
          variant="danger"
          className="w-full text-xs font-bold mt-2"
        >
          <Trash2 size={13} />
          Remove Photograph
        </Button>
      </div>

      {/* 2. Right side: Fields and Actions */}
      <div className="flex-1 flex flex-col gap-4">
        {/* Row 1: Category dropdown */}
        <div className="flex flex-col gap-1.5">
          <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest flex items-center gap-1">
            <Layers size={12} className="text-indigo-400" />
            Inspection Category
          </label>
          <select
            value={category}
            onChange={handleCategoryChange}
            className="glass-input px-3 py-2.5 rounded-lg text-sm text-white w-full appearance-none cursor-pointer"
          >
            {categories.map((cat) => (
              <option key={cat.id} value={cat.name} className="bg-gray-950 text-white">
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        {/* Row 2: AI Actions Row */}
        <div className="flex flex-wrap gap-2.5">
          <Button
            onClick={handleAIDescribe}
            isLoading={isGenerating}
            variant="secondary"
            className="flex-1 text-xs font-bold border-indigo-900/40 text-indigo-300 bg-indigo-950/20 hover:bg-indigo-900/30"
          >
            <Wand2 size={13} />
            Generate Description (AI)
          </Button>

          <Button
            onClick={handleOCR}
            isLoading={isOCRRunning}
            variant="secondary"
            className="flex-1 text-xs font-bold border-purple-900/40 text-purple-300 bg-purple-950/20 hover:bg-purple-900/30"
          >
            <ScanText size={13} />
            Extract Text (OCR)
          </Button>
        </div>

        {/* Row 3: Description textarea */}
        <div className="flex flex-col gap-1.5 flex-grow">
          <label className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">
            Inspector Notes & Descriptions
          </label>
          <textarea
            value={description}
            onChange={handleDescChange}
            placeholder="AI description or manual inspection notes go here..."
            className="glass-input p-3 rounded-lg text-sm text-white w-full h-[95px] resize-none"
          />
        </div>

        {/* Row 4: OCR Text Display Block if available */}
        {image.ocr_text && (
          <div className="p-3 bg-gray-950/60 border border-gray-900 rounded-lg text-xs flex flex-col gap-1.5">
            <span className="font-extrabold text-purple-400 uppercase tracking-wider text-[9px] flex items-center gap-1">
              ⚡ Extracted Decal / Plate Text (OCR)
            </span>
            <p className="text-gray-400 font-mono italic leading-relaxed">
              {image.ocr_text}
            </p>
          </div>
        )}

        {/* Row 5: Save Edits button */}
        {hasUnsavedChanges && (
          <Button
            onClick={handleSave}
            variant="primary"
            className="w-full text-xs font-bold py-2 shadow-indigo-500/10"
          >
            <Save size={13} />
            Save Description Updates
          </Button>
        )}
      </div>

    </div>
  );
};
