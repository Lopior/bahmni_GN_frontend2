# Usa la imagen oficial de Python como base
FROM python:3.8-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

#instalar dependencias

RUN apt-get update && \
    apt-get install -y libgirepository1.0-dev libpango1.0-dev wkhtmltopdf \
    libcairo2  libgdk-pixbuf2.0-0 libffi-dev shared-mime-info \
    libmysqlclient-dev libjpeg-dev libopenjp2-7 libtiff5 libffi-dev libprotobuf-dev && 
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copia el archivo requirements.txt al contenedor en /app
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Set the library path
ENV LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/girepository-1.0/:$LD_LIBRARY_PATH

# Copia el contenido actual al contenedor en /app
COPY frontend/ /app

# Expone el puerto 5000 (el mismo que está configurado en tu aplicación Flask)
EXPOSE 5000

# Ejecuta los scripts cuando el contenedor se inicia
CMD ["python", "app.py"] 

