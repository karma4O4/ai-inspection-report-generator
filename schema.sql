-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Reports table
CREATE TABLE IF NOT EXISTS reports (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  site_name TEXT NOT NULL,
  client_name TEXT NOT NULL,
  report_title TEXT NOT NULL,
  inspection_date DATE NOT NULL,
  conclusion TEXT,
  pdf_url TEXT,
  status TEXT DEFAULT 'draft',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Images table
CREATE TABLE IF NOT EXISTS images (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  report_id UUID REFERENCES reports(id) ON DELETE CASCADE,
  image_url TEXT NOT NULL,
  filename TEXT NOT NULL,
  category TEXT,
  ai_description TEXT,
  edited_description TEXT,
  ocr_text TEXT,
  upload_order INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default categories
INSERT INTO categories (name, description)
VALUES
  ('Gutter Blockage', 'Debris and blockages in gutter systems'),
  ('Roof Defect', 'Damage or defects on roofing materials'),
  ('Water Damage', 'Signs of water infiltration or damage'),
  ('Structural Issue', 'Structural concerns or damage'),
  ('Siding Damage', 'Damage to exterior siding'),
  ('Foundation Issue', 'Foundation cracks or concerns'),
  ('Electrical Hazard', 'Electrical safety issues'),
  ('Plumbing Issue', 'Plumbing defects or leaks'),
  ('HVAC Concern', 'Heating and cooling system issues'),
  ('General Maintenance', 'General maintenance items')
ON CONFLICT (name) DO NOTHING;

-- Enable Row Level Security (RLS)
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE images ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;

-- Create policies for reports
CREATE POLICY "Users can insert their own reports"
  ON reports FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view their own reports"
  ON reports FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update their own reports"
  ON reports FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete their own reports"
  ON reports FOR DELETE
  USING (auth.uid() = user_id);

-- Create policies for images (joined through reports table)
CREATE POLICY "Users can insert images for their reports"
  ON images FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM reports
      WHERE reports.id = images.report_id AND reports.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can view images for their reports"
  ON images FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM reports
      WHERE reports.id = images.report_id AND reports.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can update images for their reports"
  ON images FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM reports
      WHERE reports.id = images.report_id AND reports.user_id = auth.uid()
    )
  )
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM reports
      WHERE reports.id = images.report_id AND reports.user_id = auth.uid()
    )
  );

CREATE POLICY "Users can delete images for their reports"
  ON images FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM reports
      WHERE reports.id = images.report_id AND reports.user_id = auth.uid()
    )
  );

-- Create policies for categories (public read-only, write disabled except for superusers/system)
CREATE POLICY "Anyone can view categories"
  ON categories FOR SELECT
  USING (true);
