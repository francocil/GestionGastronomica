"use client";

import { useRouter } from "next/navigation";
import { Box, Button, Typography, Paper } from "@mui/material";
import { useAuthStore } from "@/app/store/auth.store";

export default function SelectTenantPage() {
  const router = useRouter();
  const tenants = useAuthStore((s) => s.tenants);
  const setCurrentTenant = useAuthStore((s) => s.setCurrentTenant);

  const handleSelect = (tenant: any) => {
    setCurrentTenant(tenant); // ← AQUÍ SE GUARDA EL TENANT SELECCIONADO
    router.push("/(private)/dashboard");
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography
        variant="h4"
        sx={{
          fontWeight: "bold",
          color: "#5D8AA8",
          fontFamily: "Montserrat",
          mb: 3,
        }}
      >
        Seleccionar Tenant
      </Typography>

      <Paper sx={{ p: 3 }}>
        {tenants.map((tenant) => (
          <Button
            key={tenant.id}
            variant="contained"
            sx={{
              display: "block",
              mb: 2,
              backgroundColor: "#5D8AA8",
              fontFamily: "Montserrat",
              "&:hover": { backgroundColor: "#4A6E85" },
            }}
            onClick={() => handleSelect(tenant)}
          >
            {tenant.nombre}
          </Button>
        ))}
      </Paper>
    </Box>
  );
}
