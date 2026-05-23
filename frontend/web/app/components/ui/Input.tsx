"use client";

import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export default function Input(props: InputProps) {
  return (
    <input
      {...props}
      className="
        w-full h-12 px-4 rounded-md
        border border-gray-300
        focus:outline-none focus:ring-2 focus:ring-[#5D8AA8]
        text-gray-800
      "
    />
  );
}
