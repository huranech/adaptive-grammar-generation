// imports
import { useNavigate, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";

// project imports
import LearningNode from "../../components/LearningNode/LearningNode";

// services
import { deleteUser } from "../../services/databaseService";

// styles
import "./LearningTree.css";

const LearningTree = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // 🔹 usuario almacenado
  const storedUser = JSON.parse(localStorage.getItem("user")) || {};
  const { user_id, username, lessons: storedLessons = [] } = storedUser;

  // 🔹 estado local de las lecciones
  const [lessons, setLessons] = useState(storedLessons);

  // =======================================================
  // 🧩 1. Si venimos desde Stage con datos actualizados
  // =======================================================
  useEffect(() => {
    if (location.state?.lessons) {
      const { completed, unlocked } = location.state.lessons;

      const updated = lessons.map((l) => {
        if (l.name === completed) return { ...l, completed: true };
        if (unlocked.includes(l.name)) return { ...l, locked: false };
        return l;
      });

      setLessons(updated);

      localStorage.setItem(
        "user",
        JSON.stringify({ ...storedUser, lessons: updated })
      );
    }
  }, [location.state]);

  // =======================================================
  // 🧩 2. Logout
  // =======================================================
  const handleLogout = () => {
    localStorage.removeItem("user");
    navigate("/");
  };

  // =======================================================
  // 🧩 3. Eliminar usuario
  // =======================================================
  const handleDeleteUser = async () => {
    if (!user_id) return;
    const confirmDelete = window.confirm(
      "¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer."
    );
    if (!confirmDelete) return;

    try {
      const data = await deleteUser(user_id);
      alert(data.message || "Usuario eliminado");
      localStorage.removeItem("user");
      navigate("/");
    } catch (err) {
      console.error("Error al eliminar usuario:", err);
      alert("Error al eliminar usuario");
    }
  };

  // =======================================================
  // 🧩 4. Agrupar por grupo
  // =======================================================
  const lessonsByGroup = lessons.reduce((acc, lesson) => {
    const lesson_group = lesson.lesson_group || "Otros";
    if (!acc[lesson_group]) acc[lesson_group] = [];
    acc[lesson_group].push(lesson);
    return acc;
  }, {});

  return (
    <div className="learning-tree-container">
      {/* Header */}
      <header className="learning-tree-header">
        <h1 className="tree-title">🌳 Ikasi Euskara!</h1>

        <div className="header-right-buttons">
          <button className="right-btn" onClick={handleDeleteUser}>
            Eliminar usuario
          </button>
          <button className="right-btn secondary">Ayuda</button>
          <button className="left-btn" onClick={handleLogout}>
            Cerrar sesión
          </button>
        </div>
      </header>

      {/* FILAS POR GRUPO */}
      <div className="learning-tree-groups-container">
        {Object.keys(lessonsByGroup).map((lesson_group) => (
          <div key={lesson_group} className="learning-group-block">
            <h2 className="learning-group-title">{lesson_group}</h2>

            <div className="learning-group-row">
              {lessonsByGroup[lesson_group].map((lesson, idx) => (
                <LearningNode
                  key={idx}
                  nodeName={lesson.name}
                  lesson_group={lesson.lesson_group}
                  emoji={lesson.emoji}
                  unlocked={!lesson.locked}
                  completed={lesson.completed}
                  dependencies={lesson.dependencies || []}
                  user_id={user_id}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LearningTree;
