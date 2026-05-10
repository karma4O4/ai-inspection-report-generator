import { LoginForm } from "@/components/auth/LoginForm";
import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col lg:flex-row items-center justify-center p-6 lg:p-16 gap-12 max-w-7xl mx-auto">
      {/* Visual intro section */}
      <div className="flex-1 flex flex-col gap-6 max-w-xl text-center lg:text-left">
        <div className="inline-flex self-center lg:self-start items-center gap-2 px-3 py-1.5 rounded-full glass-panel border-blue-500/20 text-xs font-bold text-blue-400 uppercase tracking-widest animate-pulse-slow">
          ⚡ Powered by GPT-4 Vision & OCR
        </div>
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white leading-tight">
          Professional <span className="gradient-text">AI Inspection Reports</span> in Minutes
        </h1>
        <p className="text-base sm:text-lg text-gray-400 font-medium">
          Upload site photographs, get automated high-fidelity technical building descriptions, extract embedded text, and compile professional PDF reports on-site instantly.
        </p>
        
        <div className="hidden sm:grid grid-cols-2 gap-4 mt-4 text-left">
          <div className="p-4 rounded-xl glass-card">
            <span className="text-blue-400 font-extrabold text-xl">01. Upload Photos</span>
            <p className="text-xs text-gray-500 mt-1">Drag and drop site images (Gutters, roof, plumbing, etc.) directly in the browser.</p>
          </div>
          <div className="p-4 rounded-xl glass-card">
            <span className="text-indigo-400 font-extrabold text-xl">02. AI Vision Analysis</span>
            <p className="text-xs text-gray-500 mt-1">GPT-4 automatically inspects defects and provides actionable, engineering-grade text.</p>
          </div>
          <div className="p-4 rounded-xl glass-card">
            <span className="text-purple-400 font-extrabold text-xl">03. Extract OCR Text</span>
            <p className="text-xs text-gray-500 mt-1">Quickly extract specifications or hazard text from decals and stamps.</p>
          </div>
          <div className="p-4 rounded-xl glass-card">
            <span className="text-pink-400 font-extrabold text-xl">04. Styled PDF Export</span>
            <p className="text-xs text-gray-500 mt-1">Compile comprehensive summaries and download clean, client-ready A4 reports.</p>
          </div>
        </div>
      </div>

      {/* Authentication card container */}
      <div className="flex-1 flex justify-center items-center w-full max-w-md">
        <LoginForm />
      </div>
    </main>
  );
}
