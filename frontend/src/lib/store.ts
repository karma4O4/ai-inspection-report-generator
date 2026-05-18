import { create } from 'zustand';
import { api } from './api';
import { Report, Image, Category } from '../types';
import toast from 'react-hot-toast';

interface ReportStore {
  reports: Report[];
  currentReport: Report | null;
  categories: Category[];
  isFetchingReports: boolean;
  isFetchingReportDetails: boolean;
  isSubmittingReport: boolean;
  isUploadingImage: boolean;
  isGeneratingDescription: Record<string, boolean>; // imageId -> boolean
  isGeneratingConclusion: boolean;
  isGeneratingPDF: boolean;
  isRunningOCR: Record<string, boolean>; // imageId -> boolean
  
  // Actions
  fetchReports: () => Promise<void>;
  fetchReportDetails: (id: string) => Promise<void>;
  createReport: (report: Partial<Report>) => Promise<Report | null>;
  updateReport: (id: string, updates: Partial<Report>) => Promise<void>;
  deleteReport: (id: string) => Promise<void>;
  fetchCategories: () => Promise<void>;
  
  // Image Actions
  uploadImage: (file: File, reportId: string) => Promise<void>;
  updateImageMetadata: (id: string, updates: Partial<Image>) => Promise<void>;
  deleteImage: (id: string) => Promise<void>;
  
  // AI Actions
  generateDescription: (imageId: string, category: string) => Promise<void>;
  generateConclusion: (reportId: string) => Promise<void>;
  runOCR: (imageId: string) => Promise<void>;
  generatePDF: (reportId: string) => Promise<void>;
}

export const useStore = create<ReportStore>((set, get) => ({
  reports: [],
  currentReport: null,
  categories: [],
  isFetchingReports: false,
  isFetchingReportDetails: false,
  isSubmittingReport: false,
  isUploadingImage: false,
  isGeneratingDescription: {},
  isGeneratingConclusion: false,
  isGeneratingPDF: false,
  isRunningOCR: {},

  fetchReports: async () => {
    set({ isFetchingReports: true });
    try {
      const response = await api.get('/api/reports');
      set({ reports: response.data });
    } catch (error: any) {
      console.error("Failed to fetch reports:", error);
      toast.error(error.response?.data?.detail || "Failed to fetch reports");
    } finally {
      set({ isFetchingReports: false });
    }
  },

  fetchReportDetails: async (id: string) => {
    set({ isFetchingReportDetails: true });
    try {
      const response = await api.get(`/api/reports/${id}`);
      set({ currentReport: response.data });
    } catch (error: any) {
      console.error("Failed to fetch report details:", error);
      toast.error(error.response?.data?.detail || "Failed to fetch report details");
    } finally {
      set({ isFetchingReportDetails: false });
    }
  },

  createReport: async (reportData) => {
    set({ isSubmittingReport: true });
    try {
      const response = await api.post('/api/reports', reportData);
      set((state) => ({ reports: [response.data, ...state.reports] }));
      toast.success("Report created successfully!");
      return response.data;
    } catch (error: any) {
      console.error("Failed to create report:", error);
      toast.error(error.response?.data?.detail || "Failed to create report");
      return null;
    } finally {
      set({ isSubmittingReport: false });
    }
  },

  updateReport: async (id, updates) => {
    try {
      const response = await api.put(`/api/reports/${id}`, updates);
      set((state) => ({
        reports: state.reports.map((r) => (r.id === id ? { ...r, ...response.data } : r)),
        currentReport: state.currentReport?.id === id ? { ...state.currentReport, ...response.data } : state.currentReport,
      }));
      toast.success("Report updated successfully!");
    } catch (error: any) {
      console.error("Failed to update report:", error);
      toast.error(error.response?.data?.detail || "Failed to update report");
    }
  },

  deleteReport: async (id) => {
    try {
      await api.delete(`/api/reports/${id}`);
      set((state) => ({
        reports: state.reports.filter((r) => r.id !== id),
        currentReport: state.currentReport?.id === id ? null : state.currentReport,
      }));
      toast.success("Report deleted successfully!");
    } catch (error: any) {
      console.error("Failed to delete report:", error);
      toast.error(error.response?.data?.detail || "Failed to delete report");
    }
  },

  fetchCategories: async () => {
    try {
      const response = await api.get('/api/categories');
      set({ categories: response.data });
    } catch (error) {
      console.error("Failed to fetch categories:", error);
    }
  },

  uploadImage: async (file, reportId) => {
    set({ isUploadingImage: true });
    const toastId = toast.loading(`Uploading ${file.name}...`);
    try {
      // 1. Upload file binary
      const formData = new FormData();
      formData.append('file', file);
      
      const uploadRes = await api.post('/api/images/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      const { image_url, filename } = uploadRes.data;
      
      // 2. Save metadata to db
      const metadataPayload = {
        report_id: reportId,
        image_url,
        filename,
        category: "General Maintenance", // default category
        upload_order: (get().currentReport?.images?.length || 0) + 1
      };
      
      const dbRes = await api.post('/api/images', metadataPayload);
      
      // Update store state
      const current = get().currentReport;
      if (current && current.id === reportId) {
        const updatedImages = [...(current.images || []), dbRes.data];
        set({
          currentReport: { ...current, images: updatedImages }
        });
      }
      
      toast.success(`${file.name} uploaded successfully!`, { id: toastId });
    } catch (error: any) {
      console.error("Image upload failed:", error);
      toast.error(error.response?.data?.detail || `Failed to upload ${file.name}`, { id: toastId });
    } finally {
      set({ isUploadingImage: false });
    }
  },

  updateImageMetadata: async (id, updates) => {
    try {
      const response = await api.put(`/api/images/${id}`, updates);
      
      const current = get().currentReport;
      if (current) {
        const updatedImages = (current.images || []).map((img) => 
          img.id === id ? { ...img, ...response.data } : img
        );
        set({
          currentReport: { ...current, images: updatedImages }
        });
      }
      toast.success("Image details saved!");
    } catch (error: any) {
      console.error("Failed to update image details:", error);
      toast.error(error.response?.data?.detail || "Failed to update image details");
    }
  },

  deleteImage: async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this photo?");
    if (!confirmDelete) return;

    try {
      await api.delete(`/api/images/${id}`);
      
      const current = get().currentReport;
      if (current) {
        const updatedImages = (current.images || []).filter((img) => img.id !== id);
        set({
          currentReport: { ...current, images: updatedImages }
        });
      }
      toast.success("Image deleted successfully!");
    } catch (error: any) {
      console.error("Failed to delete image:", error);
      toast.error(error.response?.data?.detail || "Failed to delete image");
    }
  },

  generateDescription: async (imageId, category) => {
    set((state) => ({
      isGeneratingDescription: { ...state.isGeneratingDescription, [imageId]: true }
    }));
    const toastId = toast.loading("Analyzing image with AI...");
    try {
      const response = await api.post('/api/ai/analyze-image', {
        image_id: imageId,
        category
      });
      
      const current = get().currentReport;
      if (current) {
        const updatedImages = (current.images || []).map((img) => 
          img.id === imageId ? { ...img, ai_description: response.data.description, category } : img
        );
        set({
          currentReport: { ...current, images: updatedImages }
        });
      }
      toast.success("AI description generated!", { id: toastId });
    } catch (error: any) {
      console.error("AI description generation failed:", error);
      toast.error(error.response?.data?.detail || "AI analysis failed", { id: toastId });
    } finally {
      set((state) => ({
        isGeneratingDescription: { ...state.isGeneratingDescription, [imageId]: false }
      }));
    }
  },

  generateConclusion: async (reportId) => {
    set({ isGeneratingConclusion: true });
    const toastId = toast.loading("Compiling findings & generating summary...");
    try {
      const response = await api.post('/api/ai/generate-conclusion', {
        report_id: reportId
      });
      
      const current = get().currentReport;
      if (current && current.id === reportId) {
        set({
          currentReport: { ...current, conclusion: response.data.conclusion }
        });
      }
      toast.success("AI conclusion generated!", { id: toastId });
    } catch (error: any) {
      console.error("AI conclusion generation failed:", error);
      toast.error(error.response?.data?.detail || "Failed to compile conclusion", { id: toastId });
    } finally {
      set({ isGeneratingConclusion: false });
    }
  },

  runOCR: async (imageId) => {
    set((state) => ({
      isRunningOCR: { ...state.isRunningOCR, [imageId]: true }
    }));
    const toastId = toast.loading("Running OCR text extraction...");
    try {
      const response = await api.post('/api/ai/ocr', {
        image_id: imageId
      });
      
      const current = get().currentReport;
      if (current) {
        const updatedImages = (current.images || []).map((img) => 
          img.id === imageId ? { ...img, ocr_text: response.data.ocr_text } : img
        );
        set({
          currentReport: { ...current, images: updatedImages }
        });
      }
      toast.success("Text extracted successfully!", { id: toastId });
    } catch (error: any) {
      console.error("OCR extraction failed:", error);
      toast.error(error.response?.data?.detail || "OCR extraction failed", { id: toastId });
    } finally {
      set((state) => ({
        isRunningOCR: { ...state.isRunningOCR, [imageId]: false }
      }));
    }
  },

  generatePDF: async (reportId) => {
    set({ isGeneratingPDF: true });
    const toastId = toast.loading("Generating professional PDF report...");
    try {
      const response = await api.post('/api/pdf/generate', {
        report_id: reportId
      });
      
      const current = get().currentReport;
      if (current && current.id === reportId) {
        set({
          currentReport: { ...current, pdf_url: response.data.pdf_url, status: "completed" }
        });
      }
      toast.success("PDF generated successfully!", { id: toastId });
    } catch (error: any) {
      console.error("PDF generation failed:", error);
      toast.error(error.response?.data?.detail || "PDF generation failed", { id: toastId });
    } finally {
      set({ isGeneratingPDF: false });
    }
  }
}));
