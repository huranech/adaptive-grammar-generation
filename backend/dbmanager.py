# imports
import psycopg2
import os
from werkzeug.security import generate_password_hash, check_password_hash


# 🔗 conectar con la base de datos
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=5432,
        database=os.getenv("DB_NAME", "database"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASS", "admin")
    )

db_connection = psycopg2.connect(
    host="db",
    port=5432,
    database="database",
    user="admin",
    password="admin"
)

lessons = [
    {"nodeName": "Interjecciones", "lesson_group": "básicos", "emoji": "👋🏼", "unlocked": True, "dependencies": [""]},
    {"nodeName": "Repaso", "lesson_group": "básicos", "emoji": "🧠", "unlocked": False, "dependencies": ["Interjecciones"]},
    {"nodeName": "Sustantivos", "lesson_group": "básicos", "emoji": "🐈‍⬛", "unlocked": False, "dependencies": ["Interjecciones"]},
    {"nodeName": "Determinantes", "lesson_group": "determinantes y pronombres", "emoji": "🫵", "unlocked": False, "dependencies": ["Sustantivos"]},
    {"nodeName": "Vocabulario (Sustantivos)", "lesson_group": "básicos", "emoji": "🐈‍⬛", "unlocked": False, "dependencies": ["Sustantivos"]},
    {"nodeName": "Descripciones", "lesson_group": "descripciones", "emoji": "📐", "unlocked": False, "dependencies": ["Sustantivos"]},
    {"nodeName": "Genitivo", "lesson_group": "casos", "emoji": "👛", "unlocked": False, "dependencies": ["Descripciones"]},
    {"nodeName": "Vocabulario (Adjetivos)", "lesson_group": "descripciones", "emoji": "📐", "unlocked": False, "dependencies": ["Descripciones"]},
    #{"nodeName": "Negación", "lesson_group": "descripciones", "emoji": "🙅‍♂️", "unlocked": False, "dependencies": ["Descripciones"]},
    #{"nodeName": "Plural", "lesson_group": "básicos", "emoji": "🔢", "unlocked": False, "dependencies": ["Descripciones"]},
    {"nodeName": "Conjunciones", "lesson_group": "básicos", "emoji": "🔗", "unlocked": False, "dependencies": ["Sustantivos"]},
    {"nodeName": "Pronombres personales", "lesson_group": "determinantes y pronombres", "emoji": "☝️", "unlocked": False, "dependencies": ["Descripciones"]},
    {"nodeName": "Sintético intransitivo progresivo", "lesson_group": "acciones", "emoji": "🪨", "unlocked": False, "dependencies": ["Pronombres personales"]},
    #{"nodeName": "Sintético intransitivo pasado", "lesson_group": "acciones", "emoji": "🪨", "unlocked": False, "dependencies": ["Pronombres personales"]},
    #{"nodeName": "Perífrasis NOR perfectivo", "lesson_group": "acciones", "emoji": "🏃", "unlocked": False, "dependencies": ["Pronombres personales"]},
    #{"nodeName": "Perífrasis NOR imperativo", "lesson_group": "acciones", "emoji": "❗", "unlocked": False, "dependencies": ["Perífrasis NOR perfectivo"]},
    #{"nodeName": "Perífrasis NOR pasado", "lesson_group": "acciones", "emoji": "🏃", "unlocked": False, "dependencies": ["Perífrasis NOR perfectivo"]},
    #{"nodeName": "Prospección", "lesson_group": "acciones", "emoji": "🚀", "unlocked": False, "dependencies": ["Perífrasis NOR perfectivo"]},
    #{"nodeName": "Adlativo", "lesson_group": "casos", "emoji": "🏃‍♂️‍➡️", "unlocked": False, "dependencies": ["Sintético intransitivo", "Vocabulario (Sustantivos)"]}, # a ver, realmente con conocer cualquier verbo intransitivo vale
    #{"nodeName": "Inesivo", "lesson_group": "casos", "emoji": "📍", "unlocked": False, "dependencies": ["Sintético intransitivo", "Vocabulario (Sustantivos)"]}, # lo mismo
    #{"nodeName": "Ablativo", "lesson_group": "casos", "emoji": "📨", "unlocked": False, "dependencies": ["Sintético intransitivo", "Vocabulario (Sustantivos)"]}, # lo mismo
    #{"nodeName": "Comitativo", "lesson_group": "casos", "emoji": "🫂", "unlocked": False, "dependencies": ["Sintético intransitivo", "Vocabulario (Sustantivos)"]}, # lo mismo
    #{"nodeName": "Locativo", "lesson_group": "casos", "emoji": "🧭", "unlocked": False, "dependencies": ["Sintético intransitivo", "Vocabulario (Sustantivos)"]}, # lo mismo
    #{"nodeName": "Perífrasis NOR-NORI perfectivo", "lesson_group": "acciones", "emoji": "🏃", "unlocked": False, "dependencies": ["Perífrasis NOR perfectivo"]}, # y enseñar el NORI (DAT)
    #{"nodeName": "Perífrasis NOR-NORI pasado", "lesson_group": "acciones", "emoji": "🏃", "unlocked": False, "dependencies": ["Perífrasis NOR-NORI perfectivo"]},
    #{"nodeName": "Perífrasis NOR-NORK perfectivo", "lesson_group": "acciones", "emoji": "⚒️", "unlocked": False, "dependencies": ["Perífrasis NOR perfectivo"]}, # y enseñar el NORK (ERG)
    #{"nodeName": "Vocabulario (Verbos)", "lesson_group": "acciones", "emoji": "⚒️", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Benefactivo", "lesson_group": "casos", "emoji": "💰", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo", "Vocabulario (Sustantivos)"]},
    #{"nodeName": "Causativo", "lesson_group": "casos", "emoji": "🔥", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo", "Vocabulario (Sustantivos)"]},
    #{"nodeName": "Instrumental", "lesson_group": "casos", "emoji": "🔧", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo", "Vocabulario (Sustantivos)"]},
    #{"nodeName": "Verbos modales", "lesson_group": "acciones", "emoji": "✨", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Partitivo", "lesson_group": "casos", "emoji": "🏜️", "unlocked": False, "dependencies": ["Genitivo", "Perífrasis NOR-NORI perfectivo", "Negación"]},
    #{"nodeName": "Postposiciones", "lesson_group": "descripciones", "emoji": "➡️", "unlocked": False, "dependencies": ["Negación", "Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Sintético transitivo progresivo", "lesson_group": "acciones", "emoji": "🪨", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Perífrasis NOR-NORI-NORK perfectivo", "lesson_group": "acciones", "emoji": "🫴", "unlocked": False, "dependencies": ["Perífrasis NOR-NORI perfectivo", "Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Adverbios", "lesson_group": "descripciones", "emoji": "🪨", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo"]},
    #{"nodeName": "Oraciones subordinadas", "lesson_group": "acciones", "emoji": "⛓️", "unlocked": False, "dependencies": ["Perífrasis NOR-NORK perfectivo"]}, # dependen de mucho
]


# =============================================
# 👨🏻‍💻 REGISTRAR USUARIO
# =============================================
def register_user(username, password):
    try:
        db_connection = get_db_connection()

        # 🔑 Hashear contraseña
        hashed_password = generate_password_hash(password)

        # 🗄️ Insertar usuario
        with db_connection.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (username, hashed_password)
            )
            user_id = cur.fetchone()[0]
            db_connection.commit()

        # 📚 Insertar lecciones por defecto
        with db_connection.cursor() as cur:
            for lesson in lessons:
                cur.execute(
                    """
                    INSERT INTO lesson (user_id, name, lesson_group, emoji, locked, completed, dependencies)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        user_id,
                        lesson["nodeName"],
                        lesson["lesson_group"],
                        lesson["emoji"],
                        not lesson["unlocked"],
                        False,
                        lesson["dependencies"]
                    )
                )
            db_connection.commit()

        print(f"✅ Usuario '{username}' registrado con ID {user_id} y lecciones por defecto creadas")
        return user_id

    # ⚠️ Excepciones
    except psycopg2.IntegrityError:
        db_connection.rollback()
        print(f"⚠️ El nombre de usuario '{username}' ya está en uso.")
        return None

    except Exception as e:
        db_connection.rollback()
        print(f"❌ Error al registrar usuario: {e}")
        return None


# =============================================
# 🔐 INICIAR SESIÓN
# =============================================
def login(username, password):
    """
    Verifica las credenciales del usuario y devuelve toda su información:
    - Datos básicos del usuario
    - Lecciones asociadas con todos sus campos
    """
    try:
        db_connection = get_db_connection()
        with db_connection.cursor() as cur:
            # 🧍 Obtener usuario
            cur.execute(
                "SELECT id, username, password FROM users WHERE username = %s;",
                (username,)
            )
            user = cur.fetchone()

            if not user:
                print(f"⚠️ Usuario '{username}' no encontrado.")
                return None

            user_id, user_name, hashed_password = user

            # 🔑 Verificar contraseña
            if not check_password_hash(hashed_password, password):
                print("❌ Contraseña incorrecta.")
                return None

            # 📚 Obtener todas las lecciones del usuario
            cur.execute(
                """
                SELECT name, lesson_group, emoji, locked, completed, dependencies
                FROM lesson
                WHERE user_id = %s
                ORDER BY id ASC;
                """,
                (user_id,)
            )
            lessons = [
                {
                    "name": name,
                    "lesson_group": lesson_group,
                    "emoji": emoji,
                    "locked": locked,
                    "completed": completed,
                    "dependencies": dependencies
                }
                for (name, lesson_group, emoji, locked, completed, dependencies) in cur.fetchall()
            ]

            # 🧾 Construir respuesta
            user_data = {
                "user_id": user_id,
                "username": user_name,
                "lessons": lessons
            }

            print(f"✅ Usuario '{username}' inició sesión correctamente.")
            return user_data

    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        db_connection.rollback()
        return None


# =============================================
# 🗑️ ELIMINAR USUARIO
# =============================================
def delete_user(user_id):
    """
    Elimina un usuario de la base de datos si las credenciales son correctas.
    Se borrarán también todos los datos asociados (lecciones, vocabulario, estructuras, etc.)
    """
    try:
        db_connection = get_db_connection()
        with db_connection.cursor() as cur:
            # 🗑️ Eliminar usuario (cascade eliminará sus datos asociados)
            cur.execute(
                "DELETE FROM users WHERE id = %s;",
                (user_id,)
            )
            db_connection.commit()

            print(f"✅ Usuario '{user_id}' eliminado correctamente.")
            return True

    # ⚠️ excepciones
    except Exception as e:
        db_connection.rollback()
        print(f"❌ Error al eliminar usuario: {e}")
        return False


# =============================================
# 🔍 RECUPERAR CONOCIMIENTO
# =============================================
def recovery_knowledge(user_id):
    """
    Recupera toda la información lingüística del usuario:
    - Estructuras gramaticales conocidas
    - Vocabulario conocido (palabra, significado y categoría gramatical)
    """
    try:
        db_connection = get_db_connection()
        with db_connection.cursor() as cur:
            # 📘 Obtener vocabulario conocido
            cur.execute(
                """
                SELECT euskera_word, spanish_meaning, pos_label
                FROM known_vocabulary
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            known_vocab = [
                {
                    "euskera_word": eu,
                    "spanish_meaning": es,
                    "pos_label": pos
                }
                for (eu, es, pos) in cur.fetchall()
            ]

            # 📙 Obtener estructuras gramaticales conocidas
            cur.execute(
                """
                SELECT pos_label
                FROM known_structures
                WHERE user_id = %s;
                """,
                (user_id,)
            )
            known_structures = [pos for (pos,) in cur.fetchall()]

            # 🧾 Empaquetar resultado
            knowledge_data = {
                "known_structures": known_structures,
                "known_vocabulary": known_vocab
            }

            return knowledge_data

    # ⚠️ Excepciones
    except Exception as e:
        db_connection.rollback()
        print(f"❌ Error al recuperar conocimiento: {e}")
        return None


# =============================================
# 🏆 COMPLETAR LECCIÓN
# =============================================
def complete_lesson(user_id, lesson_name):
    """
    Marca `lesson_name` como completada para `user_id` y desbloquea todas las lecciones cuyas dependencias
    estén ahora completadas.

    Parámetros:
      - user_id (int)
      - lesson_name (str)

    Retorna:
      - dict con clave "unlocked" (lista de nombres desbloqueados) en caso de éxito
      - False en caso de error
    """
    try:
        db_connection = get_db_connection()
        with db_connection.cursor() as cur:
            # 1) Marcar la lección como completada
            cur.execute(
                """
                UPDATE lesson
                SET completed = TRUE
                WHERE user_id = %s AND name = %s
                RETURNING id;
                """,
                (user_id, lesson_name)
            )
            row = cur.fetchone()
            if not row:
                # No existe la lección para ese usuario
                print(f"⚠️ Lección '{lesson_name}' no encontrada para user_id={user_id}.")
                db_connection.rollback()
                return False

            # 2) Recoger nombres de lecciones completadas (set para búsqueda rápida)
            cur.execute(
                "SELECT name FROM lesson WHERE user_id = %s AND completed = TRUE;",
                (user_id,)
            )
            completed_rows = cur.fetchall()
            completed_set = {r[0] for r in completed_rows}

            # 3) Buscar lecciones que estén bloqueadas y comprobar sus dependencias
            cur.execute(
                "SELECT name, dependencies FROM lesson WHERE user_id = %s AND locked = TRUE;",
                (user_id,)
            )
            locked_rows = cur.fetchall()

            to_unlock = []
            for name, deps in locked_rows:
                # deps puede ser None o lista; normalizamos a lista vacía
                deps_list = deps or []
                # Si no tiene dependencias -> desbloquear (opcional según tu lógica)
                # Aquí consideramos que si dependencies == [] entonces no depende de nada
                if len(deps_list) == 0:
                    # si quieres que las lecciones sin dependencias ya vengan unlocked,
                    # puedes omitir esto; lo dejamos por seguridad
                    to_unlock.append(name)
                else:
                    # comprobar que todas las dependencias están en completed_set
                    if all(dep in completed_set for dep in deps_list):
                        to_unlock.append(name)

            # 4) Actualizar las lecciones a desbloqueadas
            for unlock_name in to_unlock:
                cur.execute(
                    """
                    UPDATE lesson
                    SET locked = FALSE
                    WHERE user_id = %s AND name = %s;
                    """,
                    (user_id, unlock_name)
                )

            # 5) Commit y devolver resultado
            db_connection.commit()

            print(f"✅ Lección '{lesson_name}' completada para user_id={user_id}.")
            if to_unlock:
                print(f"🔓 Desbloqueadas: {', '.join(to_unlock)}")
            else:
                print("🔒 No se desbloqueó ninguna lección nueva.")

            return {"completed": lesson_name,"unlocked": to_unlock}

    except Exception as e:
        db_connection.rollback()
        print(f"❌ Error en complete_lesson: {e}")
        return False
    

# =============================================
# 🧠 GUARDAR CONOCIMIENTO
# =============================================
def save_knowledge(user_id, lesson_name):
    """
    Guarda en la base de datos las estructuras gramaticales y el vocabulario
    obligatorios de la lección especificada.

    Parámetros:
      - user_id (int)
      - lesson_name (str)

    Retorna:
      - True si todo fue bien
      - False si hubo error
    """
    try:
        db_connection = get_db_connection()
        # 🧩 Leer archivo de lección
        with open(f"Lecciones/{lesson_name}.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("//")]

        print(lines, flush=True)
        # Buscar secciones
        try:
            idx_grammar = lines.index("mandatory_grammar")
            idx_vocab = lines.index("mandatory_vocabulary")
        except ValueError:
            print(f"❌ Error: faltan etiquetas 'mandatory_grammar' o 'mandatory_vocabulary' en {lesson_name}.")
            return False

        mandatory_grammar = lines[idx_grammar + 1 : idx_vocab]
        mandatory_vocab = lines[idx_vocab + 1 :]

        print(mandatory_grammar, flush=True)
        print(mandatory_vocab, flush=True)

        with db_connection.cursor() as cur:
            # 🧠 Guardar estructuras gramaticales
            for pos_label in mandatory_grammar:
                cur.execute(
                    """
                    INSERT INTO known_structures (user_id, pos_label)
                    VALUES (%s, %s)
                    ON CONFLICT (user_id, pos_label) DO NOTHING;
                    """,
                    (user_id, pos_label)
                )
                
            # 📘 Guardar vocabulario
            for line in mandatory_vocab:
                try:
                    pos_label, euskera_word, spanish_meaning = [x.strip() for x in line.split(",", 2)]
                except ValueError:
                    print(f"⚠️ Línea de vocabulario mal formateada en {lesson_name}: {line}")
                    continue

                cur.execute(
                    """
                    INSERT INTO known_vocabulary (user_id, euskera_word, spanish_meaning, pos_label)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id, euskera_word) DO NOTHING;
                    """,
                    (user_id, euskera_word, spanish_meaning, pos_label)
                )

            db_connection.commit()

        print(f"✅ Conocimiento de '{lesson_name}' guardado correctamente para user_id={user_id}.", flush=True)
        return True

    except Exception as e:
        db_connection.rollback()
        print(f"❌ Error en save_knowledge({lesson_name}): {e}")
        return False