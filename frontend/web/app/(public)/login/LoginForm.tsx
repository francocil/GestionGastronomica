"use client";

import { useState } from "react";
import Input from "@/app/components/ui/Input";
import Button from "@/app/components/ui/Button";
import Card from "@/app/components/ui/Card";
import { authService } from "@/app/services/auth.service";
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/app/store/auth.store";

export default function LoginForm() {
  const router = useRouter();
  const setAuth = useAuthStore((state) => state.setAuth);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: any) {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await authService.login(email, password);

      setAuth(data.user, data.tenants);

      if (data.tenants.length === 1) {
        router.push("/dashboard");
      } else {
        router.push("/select-tenant");
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al iniciar sesión");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Card>
      <h1 className="text-2xl font-montserrat font-bold text-center mb-6 text-[#5D8AA8]">
        Iniciar sesión
      </h1>

      <form onSubmit={handleLogin} className="space-y-4">
        <Input
          type="email"
          placeholder="Correo electrónico"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <Input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <p className="text-red-500 text-sm text-center">{error}</p>
        )}

        <Button loading={loading}>Ingresar</Button>
      </form>
    </Card>
  );
}
