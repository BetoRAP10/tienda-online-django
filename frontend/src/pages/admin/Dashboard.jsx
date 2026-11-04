import { useEffect, useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { getMotivationalAdvice } from "../../api/thirdparty";
import { getCountryInfo } from "../../api/soap";

export function Dashboard() {
  const { auth, logout } = useAuth();
  const user = auth?.me;

  const [advice, setAdvice] = useState(null);
  const [adviceError, setAdviceError] = useState(null);

  const [isoCode, setIsoCode] = useState("MX");
  const [country, setCountry] = useState(null);
  const [countryError, setCountryError] = useState(null);
  const [loadingCountry, setLoadingCountry] = useState(false);

  useEffect(() => {
    getMotivationalAdvice()
      .then(setAdvice)
      .catch((error) => setAdviceError(error.message));
  }, []);

  const handleConsultarPais = async (event) => {
    event.preventDefault();
    setCountryError(null);
    setCountry(null);
    setLoadingCountry(true);
    try {
      const data = await getCountryInfo(isoCode, auth.token);
      setCountry(data);
    } catch (error) {
      setCountryError(error.message);
    } finally {
      setLoadingCountry(false);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1>Dashboard</h1>
          <h3>
            Bienvenido, {user?.first_name} {user?.last_name} ({user?.email})
          </h3>
        </div>
        <button className="btn-secondary" onClick={logout}>
          Cerrar sesión
        </button>
      </header>

      <section className="widget">
        <h2>Frase del día (API de terceros &mdash; Advice Slip)</h2>
        {adviceError && <p className="form-error">{adviceError}</p>}
        {!adviceError && !advice && <p>Cargando frase...</p>}
        {advice && <blockquote className="advice-quote">&ldquo;{advice}&rdquo;</blockquote>}
      </section>

      <section className="widget">
        <h2>Consumo SOAP (Django + zeep &mdash; CountryInfoService)</h2>
        <form className="country-form" onSubmit={handleConsultarPais}>
          <label htmlFor="isoCode">Código de país (ISO)</label>
          <input
            id="isoCode"
            value={isoCode}
            onChange={(e) => setIsoCode(e.target.value)}
            placeholder="MX, US, ES, FR..."
          />
          <button type="submit" disabled={loadingCountry}>
            {loadingCountry ? "Consultando..." : "Consultar"}
          </button>
        </form>

        {countryError && <p className="form-error">{countryError}</p>}

        {country && (
          <div className="country-result">
            <p>
              <strong>País:</strong> {country.nombre} ({country.codigo_iso})
            </p>
            <p>
              <strong>Capital:</strong> {country.capital}
            </p>
            <p>
              <strong>Moneda:</strong> {country.moneda}
            </p>
            <p>
              <strong>Código telefónico:</strong> +{country.codigo_telefono}
            </p>
            <p>
              <strong>Idiomas:</strong>{" "}
              {country.idiomas.map((l) => l.nombre).join(", ")}
            </p>
            <p className="country-result__source">{country.fuente}</p>
          </div>
        )}
      </section>
    </div>
  );
}
