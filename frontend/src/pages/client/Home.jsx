import { Link } from "react-router-dom";

export function Home() {
  return (
    <div className="home-page">
      <h1>tienda_online</h1>
      <p>API de productos y categorías con autenticación JWT.</p>
      <div className="home-page__actions">
        <Link to="/login" className="btn-primary">
          Iniciar sesión
        </Link>
        <Link to="/register" className="btn-secondary">
          Crear cuenta
        </Link>
      </div>
    </div>
  );
}
