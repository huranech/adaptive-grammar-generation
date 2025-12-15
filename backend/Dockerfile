# Usa la imagen base de Python
FROM python:3.11-slim

# Evita el buffering para que los print() aparezcan en tiempo real
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia primero los requirements (mejor caché)
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto de Flask
EXPOSE 5000

# Comando por defecto para ejecutar la app directamente (sin flask run)
CMD ["python", "-u", "controller.py"]
