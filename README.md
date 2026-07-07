# 📅 Feriados LATAM API

Una API REST robusta y eficiente desarrollada con **FastAPI** para la gestión y consulta de feriados nacionales de múltiples países de Latinoamérica (Perú, Chile, Colombia, etc.). El proyecto cuenta con persistencia de datos en **PostgreSQL (Supabase)**, seguridad por tokens **JWT**, y protección contra ataques por limitación de peticiones (**Rate Limiting**).

---

## 🚀 Características Clave

*   **Arquitectura Limpia:** Separación de responsabilidades mediante Routers, Modelos, Esquemas (Pydantic) y Servicios.
*   **Base de Datos en la Nube:** Integración nativa con **Supabase (PostgreSQL)**.
*   **Seguridad Avanzada:** Autenticación de administradores mediante hashing de contraseñas (Bcrypt) y **OAuth2 con JWT**.
*   **Protección Contra Ataques (Rate Limiting):** Implementación de `slowapi` para mitigar ataques DoS / Fuerza bruta basándose en la IP real del cliente (compatible con entornos en producción tras proxies).
*   **Documentación Interactiva:** Auto-generada mediante Swagger UI (`/docs`) y ReDoc (`/redoc`).

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
*   **ORM / Base de Datos:** [SQLAlchemy](https://www.sqlalchemy.org/), PostgreSQL (Supabase)
*   **Seguridad:** Passlib (Bcrypt), PyJWT, Slowapi (Rate Limit)
*   **Entorno de Desarrollo:** Python 3.10+, [Tu Editor Favorito, ej: Zed / VS Code]

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:
*   Python 3.10 o superior.
*   Una cuenta y proyecto activo en [Supabase](https://supabase.com/) (u otra instancia de PostgreSQL).

---

## ⚙️ Configuración del Entorno

1.  **Clona este repositorio:**
    ```bash
    git clone [https://github.com/](https://github.com/)[TU_USUARIO]/[NOMBRE_REPOSITORIO].git
    cd [NOMBRE_REPOSITORIO]
    ```

2.  **Crea y activa un entorno virtual:**
    ```bash
    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # En Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto basándote en la siguiente estructura:
    ```env
    DATABASE_URL="postgresql://postgres:[TU_PASSWORD]@[TU_HOST_SUPABASE]:5432/postgres"
    SECRET_KEY="[TU_JWT_SECRET_KEY_SEGURO]"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

---

## 🏃 Enceder la API

### En Desarrollo (Local)
Para levantar el servidor local accesible solo desde tu máquina:
```bash
uvicorn main:app --reload
