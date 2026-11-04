import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate, Link } from "react-router-dom";
import { registerApi } from "../../api/auth";

export function Register() {
  const navigate = useNavigate();

  const formik = useFormik({
    initialValues: { username: "", email: "", first_name: "", last_name: "", password: "" },
    validationSchema: Yup.object({
      username: Yup.string()
        .required("El usuario es obligatorio")
        .matches(/^\S*$/, "El usuario no debe contener espacios"),
      email: Yup.string().email("Correo no válido").required("El correo es obligatorio"),
      first_name: Yup.string().required("El nombre es obligatorio"),
      last_name: Yup.string().required("El apellido es obligatorio"),
      password: Yup.string()
        .required("La contraseña es obligatoria")
        .min(8, "Mínimo 8 caracteres"),
    }),
    onSubmit: async (values, { setStatus, setSubmitting }) => {
      setStatus(null);
      try {
        await registerApi(values);
        navigate("/login");
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
        <h1>Crear cuenta</h1>
        <p className="auth-card__subtitle">Regístrate para entrar al Dashboard</p>

        <label htmlFor="username">Usuario</label>
        <input
          id="username"
          name="username"
          value={formik.values.username}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          autoComplete="off"
          spellCheck="false"
        />
        {formik.touched.username && formik.errors.username && (
          <span className="field-error">{formik.errors.username}</span>
        )}

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

        <label htmlFor="first_name">Nombre</label>
        <input
          id="first_name"
          name="first_name"
          value={formik.values.first_name}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          autoComplete="off"
          spellCheck="false"
        />
        {formik.touched.first_name && formik.errors.first_name && (
          <span className="field-error">{formik.errors.first_name}</span>
        )}

        <label htmlFor="last_name">Apellido</label>
        <input
          id="last_name"
          name="last_name"
          value={formik.values.last_name}
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          autoComplete="off"
          spellCheck="false"
        />
        {formik.touched.last_name && formik.errors.last_name && (
          <span className="field-error">{formik.errors.last_name}</span>
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
          {formik.isSubmitting ? "Creando cuenta..." : "Registrarme"}
        </button>

        <p className="auth-card__footer">
          ¿Ya tienes cuenta? <Link to="/login">Inicia sesión</Link>
        </p>
      </form>
    </div>
  );
}
