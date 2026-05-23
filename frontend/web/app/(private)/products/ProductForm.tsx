"use client";

import { useState } from "react";
import {
  Box,
  Button,
  TextField,
  FormControlLabel,
  Switch,
  Typography,
} from "@mui/material";
import { useAuthStore } from "@/app/store/auth.store";

interface ProductFormProps {
  initialData?: {
    id: number;
    nombre: string;
    descripcion: string | null;
    precio: number;
    activo: boolean;
    tenant_id: number;
  };
  onSubmit: (data: any) => Promise<void>;
  loading?: boolean;
}

export default function ProductForm({
  initialData,
  onSubmit,
  loading = false,
}: ProductFormProps) {
  const tenantId = useAuthStore((s) => s.tenant_id);

  const [nombre, setNombre] = useState(initialData?.nombre ?? "");
  const [descripcion, setDescripcion] = useState(initialData?.descripcion ?? "");
  const [precio, setPrecio] = useState(initialData?.precio ?? 0);
  const [activo, setActivo] = useState(initialData?.activo ?? true);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload = {
      nombre,
      descripcion: descripcion || null,
      precio: Number(precio),
      activo,
      tenant_id: initialData?.tenant_id ?? tenantId,
    };

    await onSubmit(payload);
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 3,
        maxWidth: 500,
      }}
    >
      <Typography
        variant="h5"
        sx={{
          fontWeight: "bold",
          color: "#5D8AA8",
          fontFamily: "Montserrat",
        }}
      >
        {initialData ? "Editar Producto" : "Nuevo Producto"}
      </Typography>

      <TextField
        label="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        required
        fullWidth
      />

      <TextField
        label="Descripción"
        value={descripcion}
        onChange={(e) => setDescripcion(e.target.value)}
        multiline
        rows={3}
        fullWidth
      />

      <TextField
        label="Precio"
        type="number"
        value={precio}
        onChange={(e) => setPrecio(e.target.value)}
        required
        fullWidth
      />

      <FormControlLabel
        control={
          <Switch
            checked={activo}
            onChange={(e) => setActivo(e.target.checked)}
          />
        }
        label="Activo"
      />

      <Button
        type="submit"
        variant="contained"
        disabled={loading}
        sx={{
          backgroundColor: "#5D8AA8",
          fontFamily: "Montserrat",
          "&:hover": { backgroundColor: "#4A6E85" },
        }}
      >
        {initialData ? "Guardar Cambios" : "Crear Producto"}
      </Button>
    </Box>
  );
}
