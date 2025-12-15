// user_api.js

const API_URL = "http://localhost:5000/user";

// Registrar usuario
export async function registerUser(username, password) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "register",
      username: username,
      password: password,
    }),
  });

  const data = await response.json();
  return data;
}


// Login de usuario
export async function loginUser(username, password) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "login",
      username: username,
      password: password,
    }),
  });

  const data = await response.json();
  return data;
}


// Eliminar usuario
export async function deleteUser(user_id) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "delete_user",
      user_id: user_id,
    }),
  });

  const data = await response.json();
  return data;
}


// actualizar árbol de aprendizaje
export async function updateLessons(user_id, lessonName) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "update_lesson",
      user_id: user_id,
      lesson_name: lessonName
    }),
  });

  const data = await response.json();
  return data;
}


// guardar conocimiento nuevo
export async function saveKnowledge(user_id, lessonName) {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      action: "save_knowledge",
      user_id: user_id,
      lesson_name: lessonName
    }),
  });

  const data = await response.json();
  return data;
}