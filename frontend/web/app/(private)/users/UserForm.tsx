"use client";

import { useState } from "react";
import Card from "@/app/components/ui/Card";
import Input from "@/app/components/ui/Input";
import Button from "@/app/components/ui/Button";

export default function UserForm({ onClose }: { onClose: () => void }) {
  const [email, setEmail] = useState("");
  const [nombre, setNombre] = useState("");
  const [apellido, setApellido] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: any) {
    e.preventDefault();
    setError("");

    const payload = {
      email,
      nombre,
      apellido,
      password,
      activo: true,
    };

    const res = await fetch("http://localhost:8000/admin/users", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const data = await res.json();
      setError(data.detail || "Error al crear usuario");
      return;
    }

    onClose();
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <Card className="w-[400px]">
        <h2 className="text-xl font-bold text-[#5D8AA8] mb-4">
          Crear usuario
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

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

          <Input
            type="password"
            placeholder="Contraseña"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={onClose}>
              Cancelar
            </Button>
            <Button type="submit">Crear</Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
