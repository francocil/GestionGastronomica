"use client";

import { useEffect, useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import {
  Box,
  Button,
  CircularProgress,
  Typography,
  Paper,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  MenuItem,
  IconButton,
  FormControlLabel,
  Checkbox,
} from "@mui/material";

import {
  DataGrid,
  type GridColDef,
  type GridRenderCellParams,
  type GridPaginationModel,
  type GridSortModel,
} from "@mui/x-data-grid";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";
import ViewCompactIcon from "@mui/icons-material/ViewCompact";
import ViewAgendaIcon from "@mui/icons-material/ViewAgenda";
import SettingsIcon from "@mui/icons-material/Settings";

import {
  getProducts,
  deleteProduct,
} from "@/app/services/products.service";

import { useToast } from "@/app/components/ui/ToastProvider";

interface Product {
  id: number;
  nombre: string;
  descripcion: string;
  precio: number;
  activo: boolean;
}

export default function ProductsPage() {
  const router = useRouter();
  const { showSuccess, showError } = useToast();

  // ============================================================
  // ESTADOS PRINCIPALES
  // ============================================================
  const [rows, setRows] = useState<Product[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  // Filtros
  const [search, setSearch] = useState("");
  const [minPrecio, setMinPrecio] = useState<string>("");
  const [maxPrecio, setMaxPrecio] = useState<string>("");
  const [activo, setActivo] = useState<string>("todos");

  // Filtros por fecha de creación
  const [fechaDesde, setFechaDesde] = useState<string>("");
  const [fechaHasta, setFechaHasta] = useState<string>("");

  // Filtros por fecha de actualización
  const [fechaActualizacionDesde, setFechaActualizacionDesde] =
    useState<string>("");
  const [fechaActualizacionHasta, setFechaActualizacionHasta] =
    useState<string>("");

  // Vista compacta
  const [compactView, setCompactView] = useState(false);

  // Columnas configurables
  const [columnConfigOpen, setColumnConfigOpen] = useState(false);
  const [visibleColumns, setVisibleColumns] = useState({
    id: true,
    nombre: true,
    descripcion: true,
    precio: true,
    activo: true,
    acciones: true,
  });

  // Column visibility model (MUI correcto)
  const [columnVisibilityModel, setColumnVisibilityModel] =
    useState<Record<string, boolean>>({
      id: true,
      nombre: true,
      descripcion: true,
      precio: true,
      activo: true,
      acciones: true,
    });

  // Paginación y ordenamiento
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: 10,
  });

  const [sortModel, setSortModel] = useState<GridSortModel>([]);

  // Modal eliminar
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [deleteLoading, setDeleteLoading] = useState(false);

  // ============================================================
  // RESET DE FILTROS
  // ============================================================
  const resetFilters = () => {
    setSearch("");
    setMinPrecio("");
    setMaxPrecio("");
    setActivo("todos");

    setFechaDesde("");
    setFechaHasta("");

    setFechaActualizacionDesde("");
    setFechaActualizacionHasta("");

    setPaginationModel({ page: 0, pageSize: paginationModel.pageSize });
  };

  // ============================================================
  // EXPORTAR CSV
  // ============================================================
  const exportCSV = () => {
    const header = "ID,Nombre,Descripción,Precio,Activo\n";
    const body = rows
      .map(
        (p) =>
          `${p.id},"${p.nombre}","${p.descripcion}",${p.precio},${
            p.activo ? "Sí" : "No"
          }`
      )
      .join("\n");

    const blob = new Blob([header + body], { type: "text/csv" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "productos.csv";
    a.click();
    URL.revokeObjectURL(url);

    showSuccess("Exportado a CSV");
  };

  // ============================================================
  // EXPORTAR EXCEL (XLSX SIMPLE)
  // ============================================================
  const exportExcel = () => {
    const header = ["ID", "Nombre", "Descripción", "Precio", "Activo"];
    const rowsData = rows.map((p) => [
      p.id,
      p.nombre,
      p.descripcion,
      p.precio,
      p.activo ? "Sí" : "No",
    ]);

    const csvContent =
      header.join(",") +
      "\n" +
      rowsData.map((r) => r.join(",")).join("\n");

    const blob = new Blob([csvContent], {
      type: "application/vnd.ms-excel",
    });

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "productos.xlsx";
    a.click();
    URL.revokeObjectURL(url);

    showSuccess("Exportado a Excel");
  };

  // ============================================================
  // VISTA COMPACTA → OCULTA DESCRIPCIÓN
  // ============================================================
  useEffect(() => {
    setColumnVisibilityModel((prev) => ({
      ...prev,
      descripcion: !compactView,
    }));
  }, [compactView]);

  // ============================================================
  // LOAD PRODUCTS (SERVER-SIDE)
  // ============================================================
  useEffect(() => {
    async function load() {
      try {
        setLoading(true);

        const sort = sortModel[0];

        const res = await getProducts({
          page: paginationModel.page + 1,
          limit: paginationModel.pageSize,
          search: search || null,
          min_precio: minPrecio ? Number(minPrecio) : null,
          max_precio: maxPrecio ? Number(maxPrecio) : null,
          activo:
            activo === "todos" ? null : activo === "true" ? true : false,
          sort_by: sort?.field ?? null,
          order: sort?.sort ?? null,

          // fechas creación
          fecha_desde: fechaDesde || null,
          fecha_hasta: fechaHasta || null,

          // fechas actualización
          fecha_actualizacion_desde:
            fechaActualizacionDesde || null,
          fecha_actualizacion_hasta:
            fechaActualizacionHasta || null,
        });

        setRows(res.items);
        setTotal(res.total);
      } catch (err) {
        console.error("Error cargando productos:", err);
        showError("Error cargando productos");
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [
    paginationModel,
    sortModel,
    search,
    minPrecio,
    maxPrecio,
    activo,
    fechaDesde,
    fechaHasta,
    fechaActualizacionDesde,
    fechaActualizacionHasta,
    showError,
  ]);

  // ============================================================
  // DELETE PRODUCT
  // ============================================================
  const handleDelete = async () => {
    if (!deleteId) return;

    try {
      setDeleteLoading(true);
      await deleteProduct(deleteId);

      showSuccess("Producto eliminado correctamente");

      const sort = sortModel[0];
      const res = await getProducts({
        page: paginationModel.page + 1,
        limit: paginationModel.pageSize,
        search: search || null,
        min_precio: minPrecio ? Number(minPrecio) : null,
        max_precio: maxPrecio ? Number(maxPrecio) : null,
        activo:
          activo === "todos" ? null : activo === "true" ? true : false,
        sort_by: sort?.field ?? null,
        order: sort?.sort ?? null,

        fecha_desde: fechaDesde || null,
        fecha_hasta: fechaHasta || null,

        fecha_actualizacion_desde:
          fechaActualizacionDesde || null,
        fecha_actualizacion_hasta:
          fechaActualizacionHasta || null,
      });

      setRows(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error("Error eliminando producto:", err);
      showError("Error al eliminar el producto");
    } finally {
      setDeleteLoading(false);
      setDeleteId(null);
    }
  };

  // ============================================================
  // COLUMNAS DINÁMICAS
  // ============================================================
  const columns: GridColDef[] = useMemo(() => {
    const cols: GridColDef[] = [];

    if (visibleColumns.id)
      cols.push({ field: "id", headerName: "ID", width: compactView ? 60 : 80 });

    if (visibleColumns.nombre)
      cols.push({ field: "nombre", headerName: "Nombre", flex: 1 });

    if (visibleColumns.descripcion)
      cols.push({
        field: "descripcion",
        headerName: "Descripción",
        flex: 1,
      });

    if (visibleColumns.precio)
      cols.push({
        field: "precio",
        headerName: "Precio",
        width: compactView ? 100 : 120,
        renderCell: (params: GridRenderCellParams) =>
          `$ ${Number((params.row as Product).precio).toFixed(2)}`,
      });

    if (visibleColumns.activo)
      cols.push({
        field: "activo",
        headerName: "Activo",
        width: compactView ? 80 : 120,
        renderCell: (params: GridRenderCellParams) =>
          (params.row as Product).activo ? "Sí" : "No",
      });

    if (visibleColumns.acciones)
      cols.push({
        field: "acciones",
        headerName: "Acciones",
        width: compactView ? 150 : 200,
        sortable: false,
        filterable: false,
        renderCell: (params: GridRenderCellParams) => {
          const row = params.row as Product;

          return (
            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                variant="outlined"
                size="small"
                onClick={() =>
                  router.push(`/private/products/${row.id}`)
                }
              >
                Editar
              </Button>

              <Button
                variant="outlined"
                color="error"
                size="small"
                startIcon={<DeleteIcon />}
                onClick={() => setDeleteId(row.id)}
              >
                Eliminar
              </Button>
            </Box>
          );
        },
      });

    return cols;
  }, [visibleColumns, compactView, router]);
  // ============================================================
  // RENDER
  // ============================================================
  return (
    <Box sx={{ p: 4 }}>
      <Typography
        variant="h4"
        sx={{
          fontWeight: "bold",
          color: "#5D8AA8",
          fontFamily: "Montserrat",
          mb: 3,
        }}
      >
        Productos
      </Typography>

      {/* SEARCH + FILTERS + EXPORT + VIEW MODE + COLUMN CONFIG */}
      <Paper sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
          <TextField
            label="Buscar por nombre"
            value={search}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setSearch(e.target.value);
            }}
            sx={{ width: 250 }}
          />

          <TextField
            label="Precio mínimo"
            type="number"
            value={minPrecio}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setMinPrecio(e.target.value);
            }}
            sx={{ width: 150 }}
          />

          <TextField
            label="Precio máximo"
            type="number"
            value={maxPrecio}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setMaxPrecio(e.target.value);
            }}
            sx={{ width: 150 }}
          />

          {/* FECHAS DE CREACIÓN */}
          <TextField
            label="Creado desde"
            type="date"
            value={fechaDesde}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setFechaDesde(e.target.value);
            }}
            InputLabelProps={{ shrink: true }}
            sx={{ width: 180 }}
          />

          <TextField
            label="Creado hasta"
            type="date"
            value={fechaHasta}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setFechaHasta(e.target.value);
            }}
            InputLabelProps={{ shrink: true }}
            sx={{ width: 180 }}
          />

          {/* FECHAS DE ACTUALIZACIÓN */}
          <TextField
            label="Actualizado desde"
            type="date"
            value={fechaActualizacionDesde}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setFechaActualizacionDesde(e.target.value);
            }}
            InputLabelProps={{ shrink: true }}
            sx={{ width: 180 }}
          />

          <TextField
            label="Actualizado hasta"
            type="date"
            value={fechaActualizacionHasta}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setFechaActualizacionHasta(e.target.value);
            }}
            InputLabelProps={{ shrink: true }}
            sx={{ width: 180 }}
          />

          <TextField
            select
            label="Activo"
            value={activo}
            onChange={(e) => {
              setPaginationModel((prev) => ({ ...prev, page: 0 }));
              setActivo(e.target.value);
            }}
            sx={{ width: 150 }}
          >
            <MenuItem value="todos">Todos</MenuItem>
            <MenuItem value="true">Sí</MenuItem>
            <MenuItem value="false">No</MenuItem>
          </TextField>

          <Button
            variant="outlined"
            onClick={resetFilters}
            sx={{ height: 56 }}
          >
            Reset
          </Button>

          <Box sx={{ flexGrow: 1 }} />

          {/* EXPORT */}
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={exportCSV}
            sx={{ height: 56 }}
          >
            CSV
          </Button>

          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            onClick={exportExcel}
            sx={{ height: 56 }}
          >
            Excel
          </Button>

          {/* VIEW MODE */}
          <IconButton
            onClick={() => setCompactView((v) => !v)}
            sx={{ height: 56, width: 56 }}
          >
            {compactView ? <ViewAgendaIcon /> : <ViewCompactIcon />}
          </IconButton>

          {/* COLUMN CONFIG */}
          <IconButton
            onClick={() => setColumnConfigOpen(true)}
            sx={{ height: 56, width: 56 }}
          >
            <SettingsIcon />
          </IconButton>

          {/* NEW PRODUCT */}
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            sx={{
              backgroundColor: "#5D8AA8",
              fontFamily: "Montserrat",
              height: 56,
              "&:hover": { backgroundColor: "#4A6E85" },
            }}
            onClick={() => router.push("/private/products/create")}
          >
            Nuevo Producto
          </Button>
        </Box>
      </Paper>

      {/* TABLE */}
      <Paper sx={{ height: 500, p: 2 }}>
        {loading ? (
          <Box
            sx={{
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <DataGrid
            rows={rows}
            columns={columns}
            paginationMode="server"
            sortingMode="server"
            rowCount={total}
            paginationModel={paginationModel}
            onPaginationModelChange={setPaginationModel}
            sortModel={sortModel}
            onSortModelChange={setSortModel}
            pageSizeOptions={[10, 25, 50]}
            density={compactView ? "compact" : "standard"}
            columnVisibilityModel={columnVisibilityModel}
            onColumnVisibilityModelChange={(model) =>
              setColumnVisibilityModel(model)
            }
          />
        )}
      </Paper>

      {/* DELETE CONFIRMATION */}
      <Dialog open={deleteId !== null} onClose={() => setDeleteId(null)}>
        <DialogTitle>Eliminar Producto</DialogTitle>
        <DialogContent>
          ¿Estás seguro de que querés eliminar este producto?
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteId(null)}>Cancelar</Button>
          <Button
            color="error"
            onClick={handleDelete}
            disabled={deleteLoading}
          >
            {deleteLoading ? "Eliminando..." : "Eliminar"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* COLUMN CONFIG MODAL */}
      <Dialog
        open={columnConfigOpen}
        onClose={() => setColumnConfigOpen(false)}
      >
        <DialogTitle>Columnas visibles</DialogTitle>
        <DialogContent>
          {Object.keys(visibleColumns).map((col) => (
            <FormControlLabel
              key={col}
              control={
                <Checkbox
                  checked={visibleColumns[col as keyof typeof visibleColumns]}
                  onChange={(e) =>
                    setVisibleColumns((prev) => ({
                      ...prev,
                      [col]: e.target.checked,
                    }))
                  }
                />
              }
              label={col}
            />
          ))}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setColumnConfigOpen(false)}>Cerrar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
