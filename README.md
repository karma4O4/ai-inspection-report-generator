# AI Inspection Report Generator

A tool to help building inspectors generate structured property inspection reports. Built with FastAPI, Next.js, OpenAI GPT-4o Vision, PaddleOCR, and Supabase.

---

## Overview

This tool lets building inspectors quickly generate PDF reports from site visits:
- Create workspaces for specific clients, sites, and dates.
- Upload photos of structural defects, HVAC units, roof issues, etc.
- Run GPT-4o Vision to get structured engineering descriptions of the issues.
- Extract equipment plate details using PaddleOCR.
- Compile findings into a typed executive summary.
- Export clean, printable A4 PDF reports with photo evidence and metadata tables.

---

## Features

- **Inspection Workspaces**: Keep photos and metadata organized by site and client.
- **Drag-and-Drop Uploader**: Direct upload with image validation (supports format checks and file size limits).
- **GPT-4o Vision integration**: Categorized defect analysis (Roof Defect, Gutter Blockage, HVAC, etc.).
- **OCR extraction**: OCR parser to extract serial numbers and spec text from equipment plates.
- **AI Executive Summary**: Generates a brief technical summary based on the uploaded findings.
- **A4 PDF Export**: Formatted layout engine using ReportLab, complete with page numbering, running headers, and image grids.
- **Authentication & Security**: Supabase auth coupled with Row-Level Security (RLS) policies.
- **Storage Fallbacks**: Uses Cloudinary for cloud hosting with a local filesystem fallback.
- **Dockerized**: Container configuration included for simple backend hosting.

---

## Project Structure

```
ai-inspection-report/
├── backend/                          # FastAPI Backend
│   ├── main.py                       # App entry point, CORS, static routes
│   ├── Dockerfile                    # Production container setup
│   ├── requirements.txt              # Backend dependencies
│   ├── .env.example                  # Environment configuration template
│   ├── models/
│   │   └── schemas.py                # Pydantic schemas
│   ├── routers/
│   │   ├── auth.py                   # Auth proxy routes
│   │   ├── reports.py                # Reports CRUD
│   │   ├── images.py                 # Image uploads
│   │   ├── ai.py                     # GPT-4o Vision & PaddleOCR endpoints
│   │   └── pdf.py                    # PDF compiler & download route
│   ├── services/
│   │   ├── openai_service.py         # OpenAI GPT-4o wrappers
│   │   ├── ocr_service.py            # PaddleOCR integration
│   │   ├── pdf_service.py            # ReportLab A4 PDF builder
│   │   └── storage_service.py        # Cloudinary and filesystem adapters
│   └── utils/
│       ├── auth.py                   # JWT verification
│       └── database.py               # Supabase DB client helper
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # App router layout & pages
│   │   │   ├── page.tsx              # Login / Landing page
│   │   │   ├── dashboard/            # Projects list
│   │   │   └── reports/[id]/         # Project report workspace
│   │   ├── components/
│   │   │   ├── auth/                 # Forms for logging in & signing up
│   │   │   ├── images/               # Image dropzone & AI analysis cards
│   │   │   ├── reports/              # Report creators & lists
│   │   │   └── ui/                   # Core buttons, inputs, dialogs
│   │   ├── lib/
│   │   │   ├── api.ts                # Axios network instance
│   │   │   ├── store.ts              # Zustand store for state management
│   │   │   └── supabase.ts           # Supabase browser client
│   │   └── types/
│   │       └── index.ts              # Shared TypeScript interfaces
│   ├── .env.local.example            # Frontend environment template
│   └── package.json                  # Frontend packages
└── schema.sql                        # Database tables, keys, and RLS policies
```

---

## Technical Stack

### Backend
- **FastAPI**: Async web server
- **Supabase (PostgreSQL)**: Database, Auth, and row-level security
- **OpenAI GPT-4o**: Vision-based analysis & summaries
- **PaddleOCR**: Local image text extraction
- **ReportLab**: PDF generator
- **Cloudinary**: Cloud asset storage (optional)

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Shared type definitions
- **Tailwind CSS**: UI styling
- **Zustand**: Client-side state
- **React Dropzone**: Drag-and-drop file imports

---

## Setup & Running Locally

### 1. Database Configuration
1. Spin up a new database on [Supabase](https://supabase.com).
2. Open the SQL editor and execute the query inside `schema.sql`.
3. This creates the tables (`reports`, `images`, `categories`) and sets up Row-Level Security policies.

### 2. Run the Backend

```bash
cd backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Configure settings
cp .env.example .env
# Fill in your database URL, OpenAI key, JWT secrets, etc.

# Start development server
uvicorn main:app --reload
```

The API docs will be available at `http://localhost:8000/docs`.

### 3. Run the Frontend

```bash
cd frontend

# Install packages
npm install

# Setup env variables
cp .env.local.example .env.local
# Make sure the Supabase keys and API URLs are configured correctly

# Start the dev server
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## Environment Variables

### Backend (`backend/.env`)

```env
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development

# JWT Secrets (used for securing router paths)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# AI and OCR
OPENAI_API_KEY=sk-proj-your-key-here

# Optional Storage CDN (fallback to local folder if not configured)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Security Details

- **Row-Level Security (RLS)**: Policies check that the database queries match `auth.uid() = user_id`, keeping different users' reports isolated.
- **JWT Authorization**: Requests to the FastAPI endpoints must include the Authorization Bearer header. The backend validates this token directly with Supabase before resolving queries.
- **File Validation**: Image sizes and formats are checked to prevent arbitrary file execution.

---

## Docker

If you want to run the backend in a container:

```bash
cd backend
docker build -t ai-inspector-backend .
docker run -p 8000:8000 --env-file .env ai-inspector-backend
```

---

## License

This project is licensed under the [MIT License](LICENSE).
