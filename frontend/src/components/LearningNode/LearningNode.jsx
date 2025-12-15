import { useNavigate } from "react-router-dom";
import { useState } from "react";
import "./LearningNode.css";

const LearningNode = ({ nodeName, emoji, unlocked, completed, user_id, dependencies = [] }) => {
  const navigate = useNavigate();
  const [tooltipVisible, setTooltipVisible] = useState(false);

  const displayEmoji = unlocked ? emoji : "🔒";

  // Navegar al stage solo si está desbloqueado
  const goToStage = () => {
    if (unlocked) {
      navigate("/Stage", { state: { lessonName: nodeName, user_id } });
    }
  };

  // Solo permitir mostrar dependencias si la lección está bloqueada
  const canShowDependencies = !unlocked && dependencies.length > 0;

  return (
    <>
      <div
        className={`learning-node 
          ${unlocked ? "unlocked" : "locked"} 
          ${completed ? "completed" : ""}`}
        onClick={goToStage}
      >
        <span className="emoji">{displayEmoji}</span>
        <span className="node-name">{nodeName}</span>

        {canShowDependencies && (
          <button
            className="expand-btn"
            onClick={(e) => {
              e.stopPropagation();
              setTooltipVisible(true);
            }}
          >
            Dependencias
          </button>
        )}
      </div>

      {canShowDependencies && tooltipVisible && (
        <div className="dependencies-overlay" onClick={() => setTooltipVisible(false)}>
          <div className="dependencies-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Dependencias de {nodeName}</h3>
            <ul>
              {dependencies.map((dep, idx) => (
                <li key={idx}>{dep}</li>
              ))}
            </ul>
            <button className="close-btn" onClick={() => setTooltipVisible(false)}>
              Cerrar
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default LearningNode;
