import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api", // 🔥 prefijo /api agregado
  withCredentials: true,
  headers: {
    "X-Client-Type": "web",
  },
});

export const authService = {
  async login(email: string, password: string) {
    const res = await api.post("/auth/login", { email, password });
    return res.data;
  },

  async getMe() {
    const res = await api.get("/auth/me");
    return res.data;
  },

  async selectTenant(tenantId: number) {
    const res = await api.post("/auth/select-tenant", { tenant_id: tenantId });
    return res.data;
  },
};
