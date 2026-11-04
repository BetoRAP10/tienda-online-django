import { createContext, useEffect, useState } from "react";
import { getMeApi } from "../api/auth";
import { getToken, removeToken, setToken as persistToken } from "../api/token";

export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
});

export function AuthProvider({ children }) {
  // undefined = todavia no se sabe, null = no autenticado, objeto = autenticado
  const [auth, setAuth] = useState(undefined);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setAuth(null);
      return;
    }
    login(token);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = async (token) => {
    try {
      persistToken(token);
      const me = await getMeApi(token);
      setAuth({ token, me });
    } catch (error) {
      removeToken();
      setAuth(null);
    }
  };

  const logout = () => {
    setAuth(null);
    removeToken();
  };

  const value = { auth, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
