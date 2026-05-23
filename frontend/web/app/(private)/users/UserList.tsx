"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Button from "@/app/components/ui/Button";
import Input from "@/app/components/ui/Input";
import UserForm from "./UserForm";
import UserEditForm from "./UserEditForm";
import UserRolesForm from "./UserRolesForm";
import UserTenantsForm from "./UserTenantsForm";

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [filtered, setFiltered] = useState([]);

  const [loading, setLoading] = useState(true);

  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] = useState<any | null>(null);
  const [editingRolesUser, setEditingRolesUser] = useState<any | null>(null);
  const [editingTenantsUser, setEditingTenantsUser] = useState<any | null>(null);

  // PAGINADO
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);

  // BÚSQUEDA AVANZADA
  const [emailFilter, setEmailFilter] = useState("");
  const [nombreFilter, setNombreFilter] = useState("");
  const [apellidoFilter, setApellidoFilter] = useState("");
  const [estadoFilter, setEstadoFilter] = useState("todos"); // todos | activos | inactivos
  const [tenantFilter, setTenantFilter] = useState("todos");
  const [roleFilter, setRoleFilter] = useState("todos");

  const [tenants, setTenants] = useState([]);
  const [roles, setRoles] = useState([]);

  async function loadUsers() {
    setLoading(true);

    const skip = (page - 1) * limit;

    try {
      const res = await fetch(
        `http://localhost:8000/admin/users?skip=${skip}&limit=${limit}`,
        { credentials: "include" }
      );

      const data = await res.json();
      setUsers(data);
      setFiltered(data);
    } finally {
      setLoading(false);
    }
  }

  async function loadFiltersData() {
    const tenantsRes = await fetch("http://localhost:8000/admin/tenants", {
      credentials: "include",
    });
    const tenantsData = await tenantsRes.json();
    setTenants(tenantsData);

    const rolesRes = await fetch("http://localhost:8000/admin/roles", {
      credentials: "include",
    });
    const rolesData = await rolesRes.json();
    setRoles(rolesData);
  }

  // FILTRADO AVANZADO
  useEffect(() => {
    let result = [...users];

    if (emailFilter.trim() !== "") {
      result = result.filter((u: any) =>
        u.email.toLowerCase().includes(emailFilter.toLowerCase())
      );
    }

    if (nombreFilter.trim() !== "") {
      result = result.filter((u: any) =>
        u.nombre.toLowerCase().includes(nombreFilter.toLowerCase())
      );
    }

    if (apellidoFilter.trim() !== "") {
      result = result.filter((u: any) =>
        u.apellido.toLowerCase().includes(apellidoFilter.toLowerCase())
      );
    }

    if (estadoFilter !== "todos") {
      const activo = estadoFilter === "activos";
      result = result.filter((u: any) => u.activo === activo);
    }

    if (tenantFilter !== "todos") {
      result = result.filter((u: any) =>
        u.tenants?.some((t: any) => t.id === Number(tenantFilter))
      );
    }

    if (roleFilter !== "todos") {
      result = result.filter((u: any) =>
        u.roles?.some((r: any) => r.id === Number(roleFilter))
      );
    }

    setFiltered(result);
  }, [
    emailFilter,
    nombreFilter,
    apellidoFilter,
    estadoFilter,
    tenantFilter,
    roleFilter,
    users,
  ]);

  async function toggleActive(id: number, active: boolean) {
    await fetch(
      `http://localhost:8000/admin/users/${id}/${active ? "deactivate" : "activate"}`,
      {
        method: "PATCH",
        credentials: "include",
      }
    );
    loadUsers();
  }

  useEffect(() => {
    loadUsers();
    loadFiltersData();
  }, [page]);

  return (
    <div>
      {/* FILTROS AVANZADOS */}
      <div className="bg-gray-50 p-4 rounded-lg mb-6 border space-y-4">
        <h2 className="text-lg font-semibold text-[#5D8AA8]">Filtros avanzados</h2>

        <div className="grid grid-cols-3 gap-4">
          <Input
            placeholder="Email"
            value={emailFilter}
            onChange={(e) => setEmailFilter(e.target.value)}
          />

          <Input
            placeholder="Nombre"
            value={nombreFilter}
            onChange={(e) => setNombreFilter(e.target.value)}
          />

          <Input
            placeholder="Apellido"
            value={apellidoFilter}
            onChange={(e) => setApellidoFilter(e.target.value)}
          />

          <select
            className="border p-2 rounded"
            value={estadoFilter}
            onChange={(e) => setEstadoFilter(e.target.value)}
          >
            <option value="todos">Todos</option>
            <option value="activos">Activos</option>
            <option value="inactivos">Inactivos</option>
          </select>

          <select
            className="border p-2 rounded"
            value={tenantFilter}
            onChange={(e) => setTenantFilter(e.target.value)}
          >
            <option value="todos">Todos los tenants</option>
            {tenants.map((t: any) => (
              <option key={t.id} value={t.id}>
                {t.nombre}
              </option>
            ))}
          </select>

          <select
            className="border p-2 rounded"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
          >
            <option value="todos">Todos los roles</option>
            {roles.map((r: any) => (
              <option key={r.id} value={r.id}>
                {r.nombre}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-end">
          <Button
            variant="secondary"
            onClick={() => {
              setEmailFilter("");
              setNombreFilter("");
              setApellidoFilter("");
              setEstadoFilter("todos");
              setTenantFilter("todos");
              setRoleFilter("todos");
            }}
          >
            Limpiar filtros
          </Button>
        </div>
      </div>

      {/* HEADER */}
      <div className="flex justify-end mb-4">
        <Button onClick={() => setShowForm(true)}>Crear usuario</Button>
      </div>

      {loading ? (
        <p>Cargando usuarios...</p>
      ) : (
        <>
          <table className="w-full border-collapse">
            <thead>
              <tr className="bg-gray-100 text-left">
                <th className="p-3">ID</th>
                <th className="p-3">Email</th>
                <th className="p-3">Nombre</th>
                <th className="p-3">Apellido</th>
                <th className="p-3">Activo</th>
                <th className="p-3">Acciones</th>
              </tr>
            </thead>

            <tbody>
              {filtered.map((u: any) => (
                <tr key={u.id} className="border-b">
                  <td className="p-3">{u.id}</td>

                  <td className="p-3">
                    <Link
                      href={`/users/${u.id}`}
                      className="text-blue-600 underline hover:text-blue-800"
                    >
                      {u.email}
                    </Link>
                  </td>

                  <td className="p-3">{u.nombre}</td>
                  <td className="p-3">{u.apellido}</td>

                  <td className="p-3">
                    {u.activo ? (
                      <span className="text-green-600 font-bold">Sí</span>
                    ) : (
                      <span className="text-red-600 font-bold">No</span>
                    )}
                  </td>

                  <td className="p-3 flex gap-2">
                    <Button
                      variant="secondary"
                      onClick={() => setEditingUser(u)}
                    >
                      Editar
                    </Button>

                    <Button
                      variant="secondary"
                      onClick={() => setEditingRolesUser(u)}
                    >
                      Roles
                    </Button>

                    <Button
                      variant="secondary"
                      onClick={() => setEditingTenantsUser(u)}
                    >
                      Tenants
                    </Button>

                    <Button
                      variant="secondary"
                      onClick={() => toggleActive(u.id, u.activo)}
                    >
                      {u.activo ? "Desactivar" : "Activar"}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* PAGINADO */}
          <div className="flex justify-between items-center mt-6">
            <Button
              variant="secondary"
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
            >
              Anterior
            </Button>

            <span className="font-medium">Página {page}</span>

            <Button
              variant="secondary"
              disabled={users.length < limit}
              onClick={() => setPage(page + 1)}
            >
              Siguiente
            </Button>
          </div>
        </>
      )}

      {/* MODALES */}
      {showForm && (
        <UserForm
          onClose={() => {
            setShowForm(false);
            loadUsers();
          }}
        />
      )}

      {editingUser && (
        <UserEditForm
          user={editingUser}
          onClose={() => {
            setEditingUser(null);
            loadUsers();
          }}
        />
      )}

      {editingRolesUser && (
        <UserRolesForm
          user={editingRolesUser}
          onClose={() => {
            setEditingRolesUser(null);
            loadUsers();
          }}
        />
      )}

      {editingTenantsUser && (
        <UserTenantsForm
          user={editingTenantsUser}
          onClose={() => {
            setEditingTenantsUser(null);
            loadUsers();
          }}
        />
      )}
    </div>
  );
}
