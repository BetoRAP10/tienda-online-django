import { Login } from "../pages/common";
import { useAuth } from "../hooks/useAuth";

export function AdminLayout({ children }) {
  const { auth } = useAuth();

  if (auth === undefined) return null; // evita el flash mientras se valida el token
  if (!auth) return <Login />;

  return <div className="admin-layout">{children}</div>;
}
