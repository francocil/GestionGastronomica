"use client";

import { createContext, useContext, useState } from "react";
import { Snackbar, Alert } from "@mui/material";

interface ToastContextType {
  showSuccess: (msg: string) => void;
  showError: (msg: string) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [severity, setSeverity] = useState<"success" | "error">("success");

  const showSuccess = (msg: string) => {
    setMessage(msg);
    setSeverity("success");
    setOpen(true);
  };

  const showError = (msg: string) => {
    setMessage(msg);
    setSeverity("error");
    setOpen(true);
  };

  return (
    <ToastContext.Provider value={{ showSuccess, showError }}>
      {children}

      <Snackbar
        open={open}
        autoHideDuration={3000}
        onClose={() => setOpen(false)}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
      >
        <Alert
          onClose={() => setOpen(false)}
          severity={severity}
          variant="filled"
          sx={{ width: "100%" }}
        >
          {message}
        </Alert>
      </Snackbar>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used inside <ToastProvider>");
  return ctx;
}
