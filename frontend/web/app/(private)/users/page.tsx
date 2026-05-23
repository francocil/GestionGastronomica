import UserList from "./UserList";

export default function UsersPage() {
  return (
    <div className="p-10">
      <h1 className="text-3xl font-montserrat font-bold text-[#5D8AA8] mb-6">
        Usuarios
      </h1>

      <UserList />
    </div>
  );
}
