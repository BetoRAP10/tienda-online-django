import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate, Link } from "react-router-dom";
import { loginApi } from "../../api/auth";
import { useAuth } from "../../hooks/useAuth";

export function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: { email: "", password: "" },
    validationSchema: Yup.object({
      email: Yup.string().email("Correo no válido").required("El correo es obligatorio"),
      password: Yup.string().required("La contraseña es obligatoria"),
    }),
    onSubmit: async (values, { setStatus, setSubmitting }) => {
      setStatus(null);
      try {
        const response = await loginApi(values);
        const { access } = response;
        // Se muestra en consola para comprobar que el token se obtuvo (ver DevTools).
        console.log("Token JWT obtenido:", access);
        await login(access);
        navigate("/dashboard");
      } catch (error) {
        setStatus(error.message);
      } finally {
        setSubmitting(false);
      }
    },
  });

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={formik.handleSubmit}>
        <h1>Iniciar sesión</h1>
        <p className="auth-card__subtitle">tienda_online &middot; panel protegido</p>

        <label htmlFor="email">Correo electrónico</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formik.values.email}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          autoComplete="off"
          spellCheck="false"
        />
        {formik.touched.email && formik.errors.email && (
          <span className="field-error">{formik.errors.email}</span>
        )}

        <label htmlFor="password">Contraseña</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formik.values.password}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          autoComplete="off"
          spellCheck="false"
        />
        {formik.touched.password && formik.errors.password && (
          <span className="field-error">{formik.errors.password}</span>
        )}

        {formik.status && <div className="form-error">{formik.status}</div>}

        <button type="submit" disabled={formik.isSubmitting}>
          {formik.isSubmitting ? "Ingresando..." : "Iniciar sesión"}
        </button>

        <p className="auth-card__footer">
          ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
        </p>
      </form>
    </div>
  );
}
