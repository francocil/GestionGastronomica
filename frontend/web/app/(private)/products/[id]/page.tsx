"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { Box, CircularProgress, Paper } from "@mui/material";

import ProductForm from "../ProductForm";
import {
  getProductById,
  updateProduct,
} from "@/app/services/products.service";
import { useToast } from "@/app/components/ui/ToastProvider";

export default function EditProductPage() {
  const router = useRouter();
  const params = useParams();
  const { showSuccess, showError } = useToast();

  const id = Number(params.id);

  const [product, setProduct] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getProductById(id);
        setProduct(data);
      } catch (err) {
        console.error("Error cargando producto:", err);
        showError("No se pudo cargar el producto");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [id, showError]);

  const handleSubmit = async (data: any) => {
    try {
      await updateProduct(id, data);
      showSuccess("Producto actualizado correctamente");
      router.push("/(private)/products");
    } catch (err) {
      console.error("Error actualizando producto:", err);
      showError("Error al actualizar el producto");
    }
  };

  if (loading) {
    return (
      <Box
        sx={{
          height: "100vh",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (!product) {
    return (
      <Box sx={{ p: 4 }}>
        <Paper sx={{ p: 4 }}>Producto no encontrado.</Paper>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 4 }}>
      <Paper sx={{ p: 4, maxWidth: 600 }}>
        <ProductForm initialData={product} onSubmit={handleSubmit} />
      </Paper>
    </Box>
  );
}
