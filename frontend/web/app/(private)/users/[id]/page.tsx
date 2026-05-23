"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Card from "@/app/components/ui/Card";
import Button from "@/app/components/ui/Button";
import UserEditForm from "../UserEditForm";
import UserRolesForm from "../UserRolesForm";
import UserTenantsForm from "../UserTenantsForm";

export default function UserDetailPage() {
  const params = useParams();
  const userId = Number(params.id);

  const [user, setUser] = useState<any | null>(null);
  const [roles, setRoles] = useState([]);
  const [tenants, setTenants] = useState([]);

  const [loading, setLoading] = useState(true);

  const [editingUser, setEditingUser] = useState<any | null>(null);
  const [editingRoles, setEditingRoles] = useState<any | null>(null);
  const [editingTenants, setEditingTenants] = useState<any | null>(null);

  async function loadData() {
    setLoading(true);

    const userRes = await fetch(
      `http://localhost:8000/admin/users/${userId}`,
      { credentials: "include" }
    );
    const userData = await userRes.json();

    const assignmentsRes = await fetch(
      `http://localhost:8000/admin/assignments/user/${userId}`,
      { credentials: "include" }
    );
    const assignments = await assignmentsRes.json();

    setUser(userData);
    setRoles(assignments.map((a: any) => a.role_name));
    setTenants(assignments.map((a: any) => a.tenant_name));

    setLoading(false);
  }

  useEffect(() => {
    loadData();
  }, []);

  if (loading || !user) {
    return <p className="p-10">Cargando usuario...</p>;
  }

  return (
    <div className="p-10">
      <h1 className="text-3xl font-montserrat font-bold text-[#5D8AA8] mb-6">
        Usuario #{user.id}
      </h1>

      <Card className="p-6 space-y-4">
        <div>
          <h2 className="text-xl font-semibold">Datos personales</h2>
          <p><strong>Email:</strong> {user.email}</p>
          <p><strong>Nombre:</strong> {user.nombre}</p>
          <p><strong>Apellido:</strong> {user.apellido}</p>
          <p>
            <strong>Estado:</strong>{" "}
            {user.activo ? (
              <span className="text-green-600 font-bold">Activo</span>
            ) : (
              <span className="text-red-600 font-bold">Inactivo</span>
            )}
          </p>
        </div>

        <div>
          <h2 className="text-xl font-semibold">Roles asignados</h2>
          {roles.length === 0 ? (
            <p className="text-gray-500">Sin roles asignados</p>
          ) : (
            <ul className="list-disc ml-6">
              {roles.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          )}
        </div>

        <div>
          <h2 className="text-xl font-semibold">Tenants asignados</h2>
          {tenants.length === 0 ? (
            <p className="text-gray-500">Sin tenants asignados</p>
          ) : (
            <ul className="list-disc ml-6">
              {tenants.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          )}
        </div>

        <div className="flex gap-3 pt-4">
          <Button variant="secondary" onClick={() => setEditingUser(user)}>
            Editar usuario
          </Button>

          <Button variant="secondary" onClick={() => setEditingRoles(user)}>
            Gestionar roles
          </Button>

          <Button variant="secondary" onClick={() => setEditingTenants(user)}>
            Gestionar tenants
          </Button>
        </div>
      </Card>

      {/* MODALES */}
      {editingUser && (
        <UserEditForm
          user={editingUser}
          onClose={() => {
            setEditingUser(null);
            loadData();
          }}
        />
      )}

      {editingRoles && (
        <UserRolesForm
          user={editingRoles}
          onClose={() => {
            setEditingRoles(null);
            loadData();
          }}
        />
      )}

      {editingTenants && (
        <UserTenantsForm
          user={editingTenants}
          onClose={() => {
            setEditingTenants(null);
            loadData();
          }}
        />
      )}
    </div>
  );
}
