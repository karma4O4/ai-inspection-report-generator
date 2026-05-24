# 🏗️ AI Inspection Report Generator

> A production-ready, full-stack AI-powered property inspection platform — built with FastAPI, Next.js 14, GPT-4o Vision, PaddleOCR, and Supabase.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat&logo=supabase&logoColor=white)](https://supabase.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 📋 Overview

The **AI Inspection Report Generator** empowers building inspectors to:

- Create and manage structured **inspection workspaces** by client, site, and date
- Upload site photos (roofs, gutters, HVAC, structural defects) via a **drag-and-drop interface**
- Automatically generate **technical engineering descriptions** using **OpenAI GPT-4o Vision**
- Extract text from equipment plates and spec labels using **PaddleOCR**
- Synthesize all findings into a professional **AI executive summary**
- Export a polished, client-ready **A4 PDF report** with headers, metadata, and photo evidence

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗂️ **Inspection Workspaces** | Create and manage multiple inspections per client, site, and audit date |
| 📸 **Drag-and-Drop Upload** | React Dropzone uploader with progress states, 5MB size cap, and format validation |
| 🤖 **GPT-4o Vision Analysis** | Category-aware AI descriptions (Roof Defect, Gutter Blockage, HVAC Concern, etc.) |
| 🔍 **PaddleOCR Integration** | Extract text from equipment plates, stamps, and spec panels |
| 📝 **AI Executive Summary** | Aggregates all photo findings into a 4–6 sentence professional conclusion |
| 📄 **ReportLab PDF Export** | A4 reports with running headers, confidential footers, metadata tables, and photo logs |
| 🔐 **JWT + RLS Security** | Supabase Row-Level Security ensures users only access their own data |
| ☁️ **Cloud Storage** | Cloudinary image hosting with local filesystem fallback |
| 🐳 **Docker Ready** | Production containerised backend with `python:3.10-slim` |
| 🔄 **Resilient Fallbacks** | Graceful degradation when OpenAI or OCR credentials are unavailable |

---

## 🏛️ Architecture

```
ai-inspection-report/
├── backend/                          # FastAPI Python API
│   ├── main.py                       # App entry point, CORS, static mounts
│   ├── Dockerfile                    # Production container (python:3.10-slim)
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variable template
│   ├── models/
│   │   └── schemas.py                # Pydantic request/response schemas
│   ├── routers/
│   │   ├── auth.py                   # Login / register proxies
│   │   ├── reports.py                # Reports CRUD
│   │   ├── images.py                 # Image upload & metadata
│   │   ├── ai.py                     # GPT-4o Vision, OCR, category endpoints
│   │   └── pdf.py                    # PDF compilation & binary download
│   ├── services/
│   │   ├── openai_service.py         # GPT-4o description & summary synthesis
│   │   ├── ocr_service.py            # PaddleOCR with CPU fallback
│   │   ├── pdf_service.py            # ReportLab A4 layout engine
│   │   └── storage_service.py        # Cloudinary + local storage adapters
│   └── utils/
│       ├── auth.py                   # JWT validation dependency
│       └── database.py               # Supabase client initializer
├── frontend/                         # Next.js 14 App Router
│   ├── src/
│   │   ├── app/                      # App Router pages & layouts
│   │   │   ├── page.tsx              # Landing / login page
│   │   │   ├── dashboard/            # Inspection workspace dashboard
│   │   │   └── reports/[id]/         # Individual report workspace
│   │   ├── components/
│   │   │   ├── auth/                 # Login & register forms
│   │   │   ├── images/               # Image upload cards & AI result display
│   │   │   ├── reports/              # Report list & creation forms
│   │   │   └── ui/                   # Shared UI primitives
│   │   ├── lib/
│   │   │   ├── api.ts                # Axios API client
│   │   │   ├── store.ts              # Zustand global state store
│   │   │   └── supabase.ts           # Supabase browser client
│   │   └── types/
│   │       └── index.ts              # Shared TypeScript types
│   ├── .env.local.example            # Frontend environment template
│   ├── next.config.mjs               # Next.js build configuration
│   ├── tailwind.config.ts            # Tailwind CSS configuration
│   └── package.json                  # NPM dependencies
└── schema.sql                        # Supabase SQL migration (tables + RLS)
```

---

## 🛠️ Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com)** — High-performance async Python API framework
- **[Supabase](https://supabase.com)** — PostgreSQL database with built-in Auth and RLS
- **[OpenAI GPT-4o](https://platform.openai.com)** — Vision-based image analysis and summarization
- **[PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)** — Text extraction from equipment plates
- **[ReportLab](https://www.reportlab.com)** — Professional A4 PDF generation
- **[Cloudinary](https://cloudinary.com)** — Cloud image storage and CDN
- **[python-jose](https://github.com/mpdavis/python-jose)** — JWT authentication

### Frontend
- **[Next.js 14](https://nextjs.org)** — React framework with App Router
- **[TypeScript](https://typescriptlang.org)** — Type-safe frontend development
- **[Tailwind CSS](https://tailwindcss.com)** — Utility-first CSS styling
- **[Zustand](https://zustand-demo.pmnd.rs)** — Lightweight global state management
- **[React Dropzone](https://react-dropzone.js.org)** — Drag-and-drop file uploads
- **[Supabase JS](https://supabase.com/docs/reference/javascript)** — Auth helpers and client SDK
- **[Axios](https://axios-http.com)** — HTTP client for API requests
- **[Lucide React](https://lucide.dev)** — Icon library
- **[react-hot-toast](https://react-hot-toast.com)** — Toast notifications

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Supabase](https://supabase.com) project
- An [OpenAI API key](https://platform.openai.com)
- (Optional) A [Cloudinary](https://cloudinary.com) account

---

### 1. Database Setup (Supabase)

1. Create a project on [Supabase](https://supabase.com)
2. Open the **SQL Editor** and run the full contents of `schema.sql`
3. This will create:
   - `reports` table — stores inspection metadata
   - `images` table — links uploaded photos to reports
   - `categories` table — pre-seeded inspection categories
   - **Row-Level Security (RLS)** policies on all tables

---

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and fill in your keys (see .env.example for all required fields)

# Start the development server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

API will be live at **http://localhost:8000**  
Interactive docs: **http://localhost:8000/docs**

---

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install npm packages
npm install

# Configure environment variables
cp .env.local.example .env.local
# Ensure NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY match your project

# Start the development server
npm run dev
```

App will be live at **http://localhost:3000**

---

## 🔑 Environment Variables

### Backend (`backend/.env`)

```env
# Server
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development

# JWT
JWT_SECRET_KEY=your-strong-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-or-service-role-key

# OpenAI
OPENAI_API_KEY=sk-proj-...

# Cloudinary (optional — local fallback used if omitted)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### Frontend (`frontend/.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

> ⚠️ **Never commit `.env` or `.env.local` files.** Only `.env.example` and `.env.local.example` are safe to commit.

---

## 🐳 Docker Deployment

Build and run the backend in a production container:

```bash
cd backend

# Build the Docker image
docker build -t ai-inspector-backend .

# Run the container with environment variables
docker run -p 8000:8000 --env-file .env ai-inspector-backend
```

The backend container:
- Uses `python:3.10-slim` base image
- Installs system dependencies for Pillow, OCR, and PDF generation
- Exposes port `8000`
- Runs via `uvicorn` in production mode

---

## 🛡️ Security

- **JWT Authentication** — All FastAPI CRUD routes validate the Bearer token via `supabase.auth.get_user(token)`
- **Row-Level Security (RLS)** — PostgreSQL policies enforce that `reports.user_id = auth.uid()` for all operations
- **Image ownership validation** — Image routes verify the parent report belongs to the requesting user
- **Environment secrets** — All sensitive keys are loaded from `.env` and never exposed in source code
- **Secrets excluded from Git** — `.gitignore` covers `.env`, `.env.local`, `*.pem`, and `*.key`

---

## 📊 Database Schema

```
reports          images              categories
──────────────   ─────────────────   ──────────────────
id (uuid PK)     id (uuid PK)        id (uuid PK)
user_id (FK)     report_id (FK)      name (unique)
site_name        image_url           description
client_name      filename            created_at
report_title     category
inspection_date  ai_description
conclusion       edited_description
pdf_url          ocr_text
status           upload_order
created_at       created_at
updated_at
```

---

## 🗂️ Inspection Categories

Pre-seeded categories available for AI analysis:

| Category | Description |
|---|---|
| Gutter Blockage | Debris and blockages in gutter systems |
| Roof Defect | Damage or defects on roofing materials |
| Water Damage | Signs of water infiltration or damage |
| Structural Issue | Structural concerns or damage |
| Siding Damage | Damage to exterior siding |
| Foundation Issue | Foundation cracks or concerns |
| Electrical Hazard | Electrical safety issues |
| Plumbing Issue | Plumbing defects or leaks |
| HVAC Concern | Heating and cooling system issues |
| General Maintenance | General maintenance items |

---

## 📁 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Authenticate user |
| `POST` | `/auth/register` | Register new user |
| `GET` | `/reports` | List all reports for user |
| `POST` | `/reports` | Create new report |
| `GET` | `/reports/{id}` | Get report by ID |
| `PUT` | `/reports/{id}` | Update report |
| `DELETE` | `/reports/{id}` | Delete report |
| `POST` | `/images/upload` | Upload image to report |
| `GET` | `/images/{report_id}` | Get images for report |
| `POST` | `/ai/describe` | Run GPT-4o Vision analysis |
| `POST` | `/ai/summarize` | Generate executive summary |
| `GET` | `/ai/categories` | List inspection categories |
| `GET` | `/pdf/{report_id}` | Generate and download PDF |

Full interactive API docs available at **http://localhost:8000/docs**

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit using conventional commits: `git commit -m "feat: add your feature"`
4. Push to your fork: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ by [karma4O4](https://github.com/karma4O4)

</div>
