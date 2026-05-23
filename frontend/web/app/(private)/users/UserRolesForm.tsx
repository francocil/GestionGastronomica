"use client";

import { useEffect, useState } from "react";
import Card from "@/app/components/ui/Card";
import Button from "@/app/components/ui/Button";

export default function UserRolesForm({
  user,
  onClose,
}: {
  user: any;
  onClose: () => void;
}) {
  const [roles, setRoles] = useState([]);
  const [assigned, setAssigned] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadData() {
    setLoading(true);

    const rolesRes = await fetch("http://localhost:8000/admin/roles", {
      credentials: "include",
    });
    const rolesData = await rolesRes.json();

    const assignedRes = await fetch(
      `http://localhost:8000/admin/assignments/user/${user.id}`,
      { credentials: "include" }
    );
    const assignedData = await assignedRes.json();

    setRoles(rolesData);
    setAssigned(assignedData.map((r: any) => r.role_id));

    setLoading(false);
  }

  async function toggleRole(roleId: number) {
    const isAssigned = assigned.includes(roleId);

    if (isAssigned) {
      await fetch(
        `http://localhost:8000/admin/assignments/user/${user.id}/role/${roleId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );
      setAssigned(assigned.filter((id) => id !== roleId));
    } else {
      await fetch(`http://localhost:8000/admin/assignments`, {
        method: "POST",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          role_id: roleId,
        }),
      });
      setAssigned([...assigned, roleId]);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <Card className="w-[450px]">
        <h2 className="text-xl font-bold text-[#5D8AA8] mb-4">
          Roles de {user.nombre} {user.apellido}
        </h2>

        {loading ? (
          <p>Cargando...</p>
        ) : (
          <div className="space-y-3">
            {roles.map((r: any) => (
              <div key={r.id} className="flex items-center justify-between">
                <span>{r.nombre}</span>

                <Button
                  variant="secondary"
                  onClick={() => toggleRole(r.id)}
                >
                  {assigned.includes(r.id) ? "Quitar" : "Asignar"}
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
