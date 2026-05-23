"use client";

import { useAuthStore } from "@/app/store/auth.store";
import { authService } from "@/app/services/auth.service";
import Card from "@/app/components/ui/Card";
import Button from "@/app/components/ui/Button";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function SelectTenantForm() {
  const router = useRouter();
  const { tenants } = useAuthStore();
  const [loading, setLoading] = useState<number | null>(null);
  const [error, setError] = useState("");

  async function handleSelectTenant(tenantId: number, index: number) {
    setLoading(index);
    setError("");

    try {
      await authService.selectTenant(tenantId);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al seleccionar tenant");
    } finally {
      setLoading(null);
    }
  }

  return (
    <Card>
      <h1 className="text-2xl font-montserrat font-bold text-center mb-6 text-[#5D8AA8]">
        Seleccionar empresa
      </h1>

      {tenants.length === 0 && (
        <p className="text-center text-gray-600">
          No se encontraron tenants. Iniciá sesión nuevamente.
        </p>
      )}

      <div className="space-y-4">
        {tenants.map((tenant, index) => (
          <Button
            key={tenant.id}
            loading={loading === index}
            onClick={() => handleSelectTenant(tenant.id, index)}
          >
            {tenant.name}
          </Button>
        ))}
      </div>

      {error && (
        <p className="text-red-500 text-sm text-center mt-4">{error}</p>
      )}
    </Card>
  );
}
