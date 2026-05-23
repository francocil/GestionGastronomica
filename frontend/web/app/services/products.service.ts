import api from "./api";

export interface ProductQueryParams {
  page?: number;
  limit?: number;
  search?: string | null;
  activo?: boolean | null;
  min_precio?: number | null;
  max_precio?: number | null;
  sort_by?: string | null;
  order?: "asc" | "desc" | null;

  fecha_desde?: string | null;
  fecha_hasta?: string | null;

  fecha_actualizacion_desde?: string | null;
  fecha_actualizacion_hasta?: string | null;
}

// ============================================================
// LISTAR PRODUCTOS (PAGINADO + FILTROS + ORDEN)
// ============================================================
export async function getProducts(params: ProductQueryParams = {}) {
  const res = await api.get("/tenant/products", { params });
  return res.data; // { total, items }
}

// ============================================================
// OBTENER PRODUCTO POR ID
// ============================================================
export async function getProductById(id: number) {
  const res = await api.get(`/tenant/products/${id}`);
  return res.data;
}

// ============================================================
// CREAR PRODUCTO
// ============================================================
export async function createProduct(data: any) {
  const res = await api.post("/tenant/products", data);
  return res.data;
}

// ============================================================
// ACTUALIZAR PRODUCTO
// ============================================================
export async function updateProduct(id: number, data: any) {
  const res = await api.put(`/tenant/products/${id}`, data);
  return res.data;
}

// ============================================================
// ELIMINAR PRODUCTO
// ============================================================
export async function deleteProduct(id: number) {
  const res = await api.delete(`/tenant/products/${id}`);
  return res.data;
}
