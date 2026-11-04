const API_URL = import.meta.env.VITE_BASE_API_URL;

// Llama al endpoint propio de Django que a su vez consume el Web Service
// SOAP publico (CountryInfoService) usando la libreria zeep.
export async function getCountryInfo(isoCode, token) {
  const url = `${API_URL}/api/soap/countries/${isoCode}/`;
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error("No se pudo consultar el servicio SOAP");
  }
  return response.json();
}
