FROM python:3.14-slim

WORKDIR /workspace

# EVITA QUE PYTHON ESCRIBA ARCHIVOS .pyc en el disco y asegura que los logs salgan
# en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

# Instalar dependencias del sistema.

# Copiar e instalar requirementos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 80

# Comando para producción usando Uvicorn
# Configure el comando para usar fastapi run, que utiliza Uvicornio debajo.
# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["fastapi", "run", "main.py", "--port", "80"]
