export default function DashboardPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#5D8AA8]">
      <div className="bg-white p-10 rounded-xl shadow-md text-center max-w-md">
        <h1 className="text-3xl font-montserrat font-bold text-[#5D8AA8] mb-4">
          Dashboard
        </h1>

        <p className="text-gray-700 text-lg">
          Bienvenido. Ya estás autenticado y tenés un tenant seleccionado.
        </p>

        <p className="text-gray-500 text-sm mt-4">
          (Este es un placeholder. Después lo reemplazamos por el dashboard real.)
        </p>
      </div>
    </div>
  );
}
