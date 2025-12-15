import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser, loginUser } from "../../services/databaseService";
import "./Index.css";

const Index = () => {
  const navigate = useNavigate();

  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [message, setMessage] = useState("");
  const [isError, setIsError] = useState(false);


  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };


  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setIsError(false);

    try {
      if (isRegister) {
        const data = await registerUser(formData.username, formData.password);
        setMessage(data.message || data.error);
        setIsError(!!data.error);
      } else {
        const data = await loginUser(formData.username, formData.password);
        if (data.user_id) {
          localStorage.setItem(
            "user",
            JSON.stringify({
              user_id: data.user_id,
              username: data.username,
              lessons: data.lessons,
            })
          );
          navigate("/LearningTree");
        } else {
          setMessage(data.error || "Error en login");
          setIsError(true);
        }
      }
    } catch (err) {
      setMessage("Error en el proceso. Inténtalo más tarde.");
      setIsError(true);
      console.error(err);
    }
  };
  

  return (
    <div className="auth-container">
      {/* Panel Izquierdo: Formulario */}
      <div className="auth-box">
        <h1 className="app-title">Ikasi Euskara!</h1>

        <form onSubmit={handleSubmit} className="auth-form">
          <h2>{isRegister ? "Crear cuenta" : "Iniciar sesión"}</h2>

          <input
            type="text"
            name="username"
            placeholder="Usuario"
            value={formData.username}
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Contraseña"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <button type="submit">
            {isRegister ? "Registrarse" : "Entrar"}
          </button>

          {message && (
            <p className={`feedback ${isError ? "error" : "success"}`}>
              {message}
            </p>
          )}
        </form>

        <p className="toggle-text">
          {isRegister ? "¿Ya tienes cuenta?" : "¿No tienes cuenta?"}{" "}
          <span onClick={() => setIsRegister(!isRegister)}>
            {isRegister ? "Inicia sesión" : "Regístrate"}
          </span>
        </p>
      </div>

      {/* Panel Derecho: Imagen */}
      <div className="auth-image">
        <img src="/images/euskadi.jpg" alt="Paisaje de Euskadi" />
      </div>
    </div>
  );
};

export default Index;
