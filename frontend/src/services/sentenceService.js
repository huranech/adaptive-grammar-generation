export async function getExercises(user_id, lessonName) {
  try {
    const response = await fetch("http://localhost:5000/generateExercise", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "get_exercises",
        lesson: lessonName,
        user_id: user_id
      }),
    });

    if (!response.ok) throw new Error("Error en la respuesta del servidor");

    const data = await response.json();

    if (Array.isArray(data)) return data;

    throw new Error("Formato inesperado de ejercicios");
  } catch (error) {
    console.error("Error al obtener los ejercicios:", error);
    return [];
  }
}

export async function validateExercise(userTranslation, solution, sentence_eu) {
  try {
    const response = await fetch("http://localhost:5000/generateExercise", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "validate_exercise",
        user_translation: userTranslation,
        solution: solution,
        sentence_eu: sentence_eu
      }),
    });

    if (!response.ok) {
      throw new Error("Error en la respuesta del servidor");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error al validar el ejercicio:", error);
    return { valid: false };
  }
}