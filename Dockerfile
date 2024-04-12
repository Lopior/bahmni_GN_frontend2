# Usa una imagen más ligera de Python como base
FROM python:3.10.13-bullseye

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias
RUN apt-get update && \
    apt-get install -y \
        libgirepository1.0-dev \
        libpango1.0-dev \
        wkhtmltopdf \
        libcairo2 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        shared-mime-info \
        libmariadb-dev-compat \
        libmariadb-dev \
        libjpeg-dev \
        libopenjp2-7 \
        libffi-dev \
        libprotobuf-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copia el archivo requirements.txt y el contenido actual al contenedor en /app
COPY requirements.txt /app/
COPY frontend/ /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Set the library path
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/girepository-1.0/:$LD_LIBRARY_PATH

# Expone el puerto 8092 (el mismo que está configurado en tu aplicación Flask)
EXPOSE 8092

# Ejecuta la aplicación cuando el contenedor se inicia
#CMD ["python", "app.py"]

# Ejecuta la aplicación usando Gunicorn en lugar del servidor predeterminado de Flask
#CMD ["gunicorn", "-b", "0.0.0.0:8092", "app:app" --reload --log-level debug]

# Establece la variable de entorno para SCRIPT_NAME
#ENV SCRIPT_NAME=/notificacion

# Inicia Gunicorn con los parámetros adecuados
CMD ["gunicorn", "-b", "0.0.0.0:8092", "app:app", "--reload", "--log-level", "debug"]

