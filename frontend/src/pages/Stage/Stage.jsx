// imports
import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";

// services
import { getExercises, validateExercise } from "../../services/sentenceService";
import { updateLessons, saveKnowledge } from "../../services/databaseService";

// styles
import "./Stage.css";

const Stage = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const [loading, setLoading] = useState(true);
  const [exercises, setExercises] = useState([]);
  const [currentExercise, setCurrentExercise] = useState(null);
  const [userTranslation, setUserTranslation] = useState("");
  const [lives, setLives] = useState(5);
  const [feedback, setFeedback] = useState(null);

  // ⭐ NUEVOS ESTADOS
  const [victory, setVictory] = useState(false);
  const [defeat, setDefeat] = useState(false);

  const totalExercises = 10;
  const lessonName = location.state?.lessonName;
  const user_id = location.state?.user_id;
  const progress = ((totalExercises - exercises.length) / totalExercises) * 100;

  // 🔄 cargar ejercicios
  useEffect(() => {
    const fetchExercises = async () => {
      setLoading(true);
      const data = await getExercises(user_id, lessonName);
      setExercises(data);
      setCurrentExercise(data[0] || null);
      setLoading(false);
    };
    fetchExercises();
  }, [lessonName]);

  // 🔚 salir
  const handleExit = () => {
    navigate("/LearningTree");
  };

  // ⏩ saltar
  const handleSkip = () => {
    if (!currentExercise) return;
    const [first, ...rest] = exercises;
    setExercises([...rest, first]);
    setCurrentExercise(rest[0] || first);
  };

  // ✅ validar
  const handleValidateExercise = async () => {
    if (!userTranslation.trim()) return;

    try {
      const result = await validateExercise(
        userTranslation,
        currentExercise.solution,
        currentExercise.sentence
      );

      if (result.valid) {
        setFeedback("correct");
      } else {
        setLives((prev) => {
          const updated = prev - 1;
          if (updated <= 1) {
            setFeedback("wrong");
          }
          return updated;
        });

        setFeedback("wrong");
      }
    } catch (error) {
      console.error("Error validando:", error);
    }
  };

  // ▶️ continuar después del feedback
  const handleContinue = async () => {
    if (feedback === "correct") {
      const [, ...remaining] = exercises;

      // 🎉 Fin de ejercicios
      if (remaining.length === 0) {
        setVictory(true);
        return;
      }

      setExercises(remaining);
      setCurrentExercise(remaining[0] || null);
    }

    if (feedback === "wrong") {
      // ❌ Derrota si no quedan vidas
      if (lives <= 1) {
        setDefeat(true);
        return;
      }

      const [first, ...rest] = exercises;
      setExercises([...rest, first]);
      setCurrentExercise(rest[0] || first);
    }

    setFeedback(null);
    setUserTranslation("");
  };

  // 💬 renderizar sentence
  const renderSentence = () => {
    if (!currentExercise) return null;
    const { sentence, seen_words, lexicon } = currentExercise;

    return sentence.map((block, index) => (
      <span key={index} className="word-wrapper">
        <span className={`word ${seen_words[index] === false ? "new-word" : ""}`}>
          {block}
          <span className="tooltip">{lexicon[index]}</span>
        </span>{" "}
      </span>
    ));
  };

  // ❤️ vidas
  const renderLives = () => {
    const hearts = [];
    for (let i = 1; i <= 5; i++) {
      hearts.push(
        <span key={i} className={`heart ${i <= lives ? "heart-full" : "heart-empty"}`}>
          {i <= lives ? "💚" : "🩶"}
        </span>
      );
    }
    return hearts;
  };

  // 🔊 audio
  const playSpeech = (audioB64) => {
    const audioBytes = Uint8Array.from(atob(audioB64), (c) => c.charCodeAt(0));
    const blob = new Blob([audioBytes], { type: "audio/wav" });
    const url = URL.createObjectURL(blob);
    new Audio(url).play();
  };

  const footerClass =
    feedback === "correct"
      ? "stage-footer correct-feedback"
      : feedback === "wrong"
      ? "stage-footer wrong-feedback"
      : "stage-footer";

  // ⏳ loading
  if (loading) {
    return (
      <div className="stage-container loading-screen">
        <p className="loading">⏳ Cargando ejercicios...</p>
        <div className="spinner"></div>
      </div>
    );
  }

  // 🎉 PANTALLA DE VICTORIA
  if (victory) {
    return (
      <div className="stage-container victory-screen">
        <h1 className="victory-title">🎉 ¡Lección completada!</h1>
        <p className="victory-text">Has terminado todos los ejercicios.</p>

        <button
          className="check-btn"
          onClick={async () => {
            await saveKnowledge(user_id, lessonName);
            const data = await updateLessons(user_id, lessonName);
            navigate("/LearningTree", { state: { user_id, lessons: data } });
          }}
        >
          Continuar
        </button>
      </div>
    );
  }

  // ❌ PANTALLA DE DERROTA
  if (defeat) {
    return (
      <div className="stage-container defeat-screen">
        <h1 className="defeat-title">💀 Te has quedado sin vidas</h1>
        <p className="defeat-text">Puedes volver a intentarlo cuando quieras.</p>

        <button
          className="check-btn defeat-btn"
          onClick={() => {
            navigate("/LearningTree", { state: { user_id } });
          }}
        >
          Continuar
        </button>
      </div>
    );
  }

  // 🎯 UI NORMAL
  return (
    <div className="stage-container">
      <header className="stage-header">
        <div className="stage-header-box">
          <button className="exit-btn" onClick={handleExit}>✖</button>

          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
          </div>

          <div className="lives">{renderLives()}</div>
        </div>
      </header>

      <main className="stage-main">
        {currentExercise ? (
          <>
            <div className="sentence-container">
              <button className="sound-btn" onClick={() => playSpeech(currentExercise.speech[0])}>
                🔊
              </button>
              <p className="sentence">{renderSentence()}</p>
            </div>

            <textarea
              className="translation-input"
              placeholder="Escribe en español"
              value={userTranslation}
              onChange={(e) => setUserTranslation(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  feedback === null ? handleValidateExercise() : handleContinue();
                }
              }}
            />
          </>
        ) : null}
      </main>

      <footer className={footerClass}>
        {feedback === null ? (
          <>
            <button className="skip-btn" onClick={handleSkip}>Saltar</button>
            <button className="check-btn" onClick={handleValidateExercise}>Comprobar</button>
          </>
        ) : feedback === "correct" ? (
          <>
            <button className="skip-btn correct-label">✅ Correcto</button>
            <button className="check-btn" onClick={handleContinue}>Continuar</button>
          </>
        ) : (
          <>
            <button className="skip-btn wrong-label">💡 {currentExercise.solution}</button>
            <button className="check-btn" onClick={handleContinue}>Continuar</button>
          </>
        )}
      </footer>
    </div>
  );
};

export default Stage;
