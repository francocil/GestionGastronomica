"use client";

import { useState } from "react";
import Card from "@/app/components/ui/Card";
import Input from "@/app/components/ui/Input";
import Button from "@/app/components/ui/Button";

export default function UserEditForm({
  user,
  onClose,
}: {
  user: any;
  onClose: () => void;
}) {
  const [nombre, setNombre] = useState(user.nombre);
  const [apellido, setApellido] = useState(user.apellido);
  const [activo, setActivo] = useState(user.activo);
  const [error, setError] = useState("");

  async function handleSubmit(e: any) {
    e.preventDefault();
    setError("");

    const payload = {
      nombre,
      apellido,
      activo,
    };

    const res = await fetch(`http://localhost:8000/admin/users/${user.id}`, {
      method: "PUT",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const data = await res.json();
      setError(data.detail || "Error al actualizar usuario");
      return;
    }

    onClose();
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <Card className="w-[400px]">
        <h2 className="text-xl font-bold text-[#5D8AA8] mb-4">
          Editar usuario
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Nombre"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />

          <Input
            placeholder="Apellido"
            value={apellido}
            onChange={(e) => setApellido(e.target.value)}
          />

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={activo}
              onChange={(e) => setActivo(e.target.checked)}
            />
            <label>Activo</label>
          </div>

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Guardar cambios</Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
