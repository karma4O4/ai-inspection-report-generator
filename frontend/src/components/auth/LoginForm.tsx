'use client';

import React, { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import toast from 'react-hot-toast';

export const LoginForm: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error("Please fill in all credentials.");
      return;
    }

    setLoading(true);
    const mode = isLogin ? "Login" : "Sign Up";
    const toastId = toast.loading(`${mode} in progress...`);

    try {
      if (isLogin) {
        // Sign In
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
        toast.success("Welcome back!", { id: toastId });
      } else {
        // Sign Up
        const { error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
        toast.success("Registration successful! You can now log in.", { id: toastId });
        setIsLogin(true);
      }
    } catch (error: any) {
      console.error(`${mode} error:`, error);
      toast.error(error.message || `${mode} failed. Please try again.`, { id: toastId });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel max-w-md w-full p-8 rounded-2xl shadow-2xl border-gray-800/80">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-extrabold text-white tracking-tight mb-2">
          {isLogin ? "Sign In" : "Create Account"}
        </h2>
        <p className="text-sm text-gray-400">
          {isLogin ? "Access your building inspection workspace" : "Get started with professional AI reports"}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        <Input
          id="email"
          label="Email Address"
          type="email"
          placeholder="inspector@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        
        <Input
          id="password"
          label="Password"
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <Button type="submit" variant="primary" className="w-full mt-2" isLoading={loading}>
          {isLogin ? "Sign In" : "Sign Up"}
        </Button>
      </form>

      <div className="mt-6 text-center text-sm">
        <span className="text-gray-500">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
        </span>
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="text-blue-400 hover:text-blue-300 font-semibold underline transition-colors"
        >
          {isLogin ? "Sign Up" : "Sign In"}
        </button>
      </div>
    </div>
  );
};
