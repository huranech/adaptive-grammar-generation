-- =========================================
-- 🧍 USUARIOS
-- =========================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- 📚 LECCIONES
-- =========================================
CREATE TABLE lesson (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    lesson_group VARCHAR(255),
    emoji VARCHAR(10),
    locked BOOLEAN NOT NULL,
    completed BOOLEAN NOT NULL,
    dependencies TEXT[],
    UNIQUE (user_id, name)
);

-- =========================================
-- 📙 ESTRUCTURAS GRAMATICALES
-- =========================================
CREATE TABLE known_structures (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    pos_label VARCHAR(20) NOT NULL,
    UNIQUE (user_id, pos_label)
);

-- =========================================
-- 📘​ VOCABULARIO CONOCIDO
-- =========================================
CREATE TABLE known_vocabulary (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    euskera_word VARCHAR(100) NOT NULL,
    spanish_meaning VARCHAR(255) NOT NULL,
    pos_label VARCHAR(20) NOT NULL,
    UNIQUE (user_id, euskera_word)
);
