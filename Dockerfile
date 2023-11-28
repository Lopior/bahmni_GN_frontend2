# Usa la imagen oficial de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor en /app
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido actual al contenedor en /app
COPY . /app

# Expone el puerto 5000 (el mismo que está configurado en tu aplicación Flask)
EXPOSE 5000

# Define la variable de entorno para Flask
ENV FLASK_APP=app.py

# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["flask", "run", "--host=0.0.0.0"]
