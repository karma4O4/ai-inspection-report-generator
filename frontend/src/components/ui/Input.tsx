import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  className = '',
  id,
  ...props
}) => {
  return (
    <div className="w-full flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-xs font-bold text-gray-400 uppercase tracking-wider">
          {label}
        </label>
      )}
      <input
        id={id}
        className={`glass-input px-3.5 py-2.5 rounded-lg text-sm text-white w-full ${error ? 'border-red-500/80 focus:border-red-500 focus:ring-red-500' : ''} ${className}`}
        {...props}
      />
      {error && (
        <span className="text-xs font-semibold text-red-400 mt-0.5">
          {error}
        </span>
      )}
    </div>
  );
};
