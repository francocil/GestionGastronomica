"use client";

import { useEffect, useState } from "react";
import Card from "@/app/components/ui/Card";
import Button from "@/app/components/ui/Button";

export default function UserTenantsForm({
  user,
  onClose,
}: {
  user: any;
  onClose: () => void;
}) {
  const [tenants, setTenants] = useState([]);
  const [assigned, setAssigned] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    setLoading(true);

    const tenantsRes = await fetch("http://localhost:8000/admin/tenants", {
      credentials: "include",
    });
    const tenantsData = await tenantsRes.json();

    const assignedRes = await fetch(
      `http://localhost:8000/admin/assignments/user/${user.id}`,
      { credentials: "include" }
    );
    const assignedData = await assignedRes.json();

    setTenants(tenantsData);
    setAssigned(assignedData.map((t: any) => t.tenant_id));

    setLoading(false);
  }

  async function toggleTenant(tenantId: number) {
    const isAssigned = assigned.includes(tenantId);

    if (isAssigned) {
      await fetch(
        `http://localhost:8000/admin/assignments/user/${user.id}/tenant/${tenantId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );
      setAssigned(assigned.filter((id) => id !== tenantId));
    } else {
      await fetch(`http://localhost:8000/admin/assignments`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          tenant_id: tenantId,
        }),
      });
      setAssigned([...assigned, tenantId]);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <Card className="w-[450px]">
        <h2 className="text-xl font-bold text-[#5D8AA8] mb-4">
          Tenants de {user.nombre} {user.apellido}
        </h2>

        {loading ? (
          <p>Cargando...</p>
        ) : (
          <div className="space-y-3">
            {tenants.map((t: any) => (
              <div key={t.id} className="flex items-center justify-between">
                <span>{t.nombre}</span>

                <Button
                  variant="secondary"
                  onClick={() => toggleTenant(t.id)}
                >
                  {assigned.includes(t.id) ? "Quitar" : "Asignar"}
                </Button>
              </div>
            ))}
          </div>
        )}

        <div className="flex justify-end mt-6">
          <Button variant="secondary" onClick={onClose}>
            Cerrar
          </Button>
        </div>
      </Card>
    </div>
  );
}
