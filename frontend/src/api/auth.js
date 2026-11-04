const API_URL = import.meta.env.VITE_BASE_API_URL;

export async function loginApi(formData) {
  const url = `${API_URL}/api/token/`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  if (response.status !== 200) {
    throw new Error("Usuario o contraseña incorrecta");
  }
  return response.json();
}

export async function registerApi(formData) {
  const url = `${API_URL}/api/auth/register/`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  });

  const result = await response.json();
  if (response.status !== 201) {
    const firstError = Object.values(result)[0];
    const message = Array.isArray(firstError) ? firstError[0] : "No se pudo crear el usuario";
    throw new Error(message);
  }
  return result;
}

export async function getMeApi(token) {
  const url = `${API_URL}/api/auth/me/`;
  const response = await fetch(url, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (response.status !== 200) {
    throw new Error("No se pudo obtener el usuario");
  }
  return response.json();
}
