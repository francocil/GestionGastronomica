import React from "react";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export default function Card({ children, className = "" }: CardProps) {
  return (
    <div className={`bg-white p-8 rounded-xl shadow-md ${className}`}>
      {children}
    </div>
  );
}
