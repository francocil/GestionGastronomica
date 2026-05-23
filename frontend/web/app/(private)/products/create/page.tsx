"use client";

import { useRouter } from "next/navigation";
import { Box, Paper } from "@mui/material";
import ProductForm from "../ProductForm";
import { createProduct } from "@/app/services/products.service";
import { useToast } from "@/app/components/ui/ToastProvider";

export default function CreateProductPage() {
  const router = useRouter();
  const { showSuccess, showError } = useToast();

  const handleSubmit = async (data: any) => {
    try {
      await createProduct(data);
      showSuccess("Producto creado correctamente");
      router.push("/(private)/products");
    } catch (err) {
      console.error("Error creando producto:", err);
      showError("Error al crear el producto");
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Paper sx={{ p: 4, maxWidth: 600 }}>
        <ProductForm onSubmit={handleSubmit} />
      </Paper>
    </Box>
  );
}
