import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: "primary" | "secondary";
}

export default function Button({
  children,
  variant = "primary",
  ...props
}: ButtonProps) {
  const base =
    "px-4 py-2 rounded-md font-medium transition-colors duration-200";

  const styles =
    variant === "secondary"
      ? "bg-gray-200 text-gray-700 hover:bg-gray-300"
      : "bg-[#5D8AA8] text-white hover:bg-[#4a6f86]";

  return (
    <button className={`${base} ${styles}`} {...props}>
      {children}
    </button>
  );
}
