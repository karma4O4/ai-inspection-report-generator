export interface User {
  id: string;
  email: string;
}

export interface Category {
  id: string;
  name: string;
  description?: string;
  created_at: string;
}

export interface Image {
  id: string;
  report_id: string;
  image_url: string;
  filename: string;
  category?: string;
  ai_description?: string;
  edited_description?: string;
  ocr_text?: string;
  upload_order: number;
  created_at: string;
}

export interface Report {
  id: string;
  user_id: string;
  site_name: string;
  client_name: string;
  report_title: string;
  inspection_date: string;
  conclusion?: string;
  pdf_url?: string;
  status: 'draft' | 'completed';
  created_at: string;
  updated_at: string;
  images?: Image[];
}
