import React from 'react';

export function Alert({ children, variant = 'default' }) {
  const variants = {
    default: 'bg-gray-700/50 border-gray-600',
    destructive: 'bg-red-500/10 border-red-500/50 text-red-500'
  };

  return (
    <div className={`p-4 rounded-lg border ${variants[variant]}`}>
      {children}
    </div>
  );
}

export function AlertDescription({ children }) {
  return <p className="text-sm">{children}</p>;
} 