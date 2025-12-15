from flask import Flask, request, jsonify
from flask_cors import CORS

# project imports
import exercise_manager
import dbmanager


app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

@app.route('/generateExercise', methods=['POST'])
def generate_exercise():
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({"error": "Falta el campo 'action'"}), 400

    action = data['action']

    if action == 'get_exercises':
        lesson = data['lesson']
        user_id = data['user_id']
        exercises = exercise_manager.generate_exercises(user_id, lesson, 10)
        return jsonify(exercises), 200
    

    if action == 'validate_exercise':
        user_translation = data.get("user_translation", "")
        solution = data.get("solution", "")
        sentence_eu = data.get("sentence_eu", "")
        validation = exercise_manager.validate_exercise(user_translation, solution, sentence_eu)
        return jsonify({"valid": validation}), 200

    else:
        return jsonify({"error": "Acción no reconocida"}), 400

@app.route('/user', methods=['POST'])
def user_controller():
    data = request.get_json()
    if not data or 'action' not in data:
        return jsonify({"error": "Falta el campo 'action'"}), 400

    action = data['action']

    if action == 'register':
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"error": "Faltan campos 'username' o 'password'"}), 400

        user_id = dbmanager.register_user(username, password)
        return jsonify({
            "message": "Usuario registrado correctamente",
            "user_id": user_id,
            "username": username
        }), 200


    elif action == 'login':
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"error": "Faltan campos 'username' o 'password'"}), 400

        user_data = dbmanager.login(username, password)
        if user_data:
            return jsonify({
                "message": "Login correcto",
                "username": username,
                "user_id": user_data["user_id"],
                "lessons": user_data["lessons"]
            }), 200
        else:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


    elif action == 'delete_user':
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "Falta campo 'username'"}), 400

        dbmanager.delete_user(user_id)
        return jsonify({"message": f"Usuario {user_id} eliminado"}), 200
    

    elif action == 'update_lesson':
        user_id = data.get('user_id')
        lesson_name = data.get('lesson_name')

        if not user_id or not lesson_name:
            return jsonify({"error": "Faltan campos 'user_id' o 'lesson_name'"}), 400
        
        result = dbmanager.complete_lesson(user_id, lesson_name)

        if result:
            return jsonify({
                "message": f"Lección '{lesson_name}' completada correctamente",
                "completed": result["completed"],
                "unlocked": result["unlocked"]
            }), 200
        else:
            return jsonify({"error": "No se pudo actualizar la lección"}), 500
        

    elif action == 'save_knowledge':
        user_id = data.get('user_id')
        lesson_name = data.get('lesson_name')

        if not user_id or not lesson_name:
            return jsonify({"error": "Faltan campos 'user_id' o 'lesson_name'"}), 400
        
        result = dbmanager.save_knowledge(user_id, lesson_name)

        if result:
            return jsonify({
                "message": f"Conocimiento de la lección '{lesson_name}' guardado correctamente",
            }), 200
        else:
            return jsonify({"error": "No se pudo actualizar la lección"}), 500

    else:
        return jsonify({"error": "Acción no reconocida"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)