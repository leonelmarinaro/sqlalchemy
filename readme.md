# Ejemplo SQLAlchemy + Alembic

Este proyecto muestra cómo utilizar SQLAlchemy junto con Alembic para gestionar migraciones de bases de datos.

## Configuración inicial

1. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install sqlalchemy alembic psycopg2-binary python-dotenv
   ```

2. Configura la base de datos:
   - Crea un archivo `.env` con la variable `DATABASE_URL`
   - Por defecto se utilizará SQLite

## Comandos de Alembic

### Crear una nueva migración automáticamente
```
alembic revision --autogenerate -m "Descripción de los cambios"
```

### Ejecutar las migraciones pendientes
```
alembic upgrade head
```

### Ver la historia de migraciones
```
alembic history
```

### Revertir la última migración
```
alembic downgrade -1
```

### Actualizar a una revisión específica
```
alembic upgrade <revision_id>
```

## Uso del proyecto

## Uso del proyecto

1. Ejecutar las migraciones: `alembic upgrade head`
2. Insertar datos de ejemplo: `python -m library_app.scripts.seed_data`
3. Consultar datos: `python -m library_app.scripts.query_data`

## Utilizar setup.py para instalar el paquete
Esto instala tu paquete en "modo editable", lo que significa que puedes modificar el código y los cambios se reflejan inmediatamente sin necesidad de reinstalar.
```
pip install -e .
```