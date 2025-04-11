from library_app.db import SessionLocal
from library_app.models.user import Author, Book


def seed_data():
    db = SessionLocal()

    # Crear autores de ejemplo
    author1 = Author(
        name="Gabriel García Márquez",
        bio="Escritor colombiano, premio Nobel de Literatura",
    )
    author2 = Author(
        name="J.K. Rowling", bio="Autora británica de la saga Harry Potter"
    )

    # Añadir autores a la sesión
    db.add(author1)
    db.add(author2)
    db.flush()  # Para obtener los IDs generados

    # Crear libros de ejemplo
    book1 = Book(
        title="Cien años de soledad",
        description="Una obra maestra del realismo mágico",
        author_id=author1.id,
        publication_year=1967,
    )
    book2 = Book(
        title="Harry Potter y la piedra filosofal",
        description="El inicio de la saga de Harry Potter",
        author_id=author2.id,
        publication_year=1997,
    )

    # Añadir libros a la sesión
    db.add(book1)
    db.add(book2)

    # Guardar cambios
    db.commit()
    db.close()

    print("Datos de ejemplo insertados correctamente")


if __name__ == "__main__":
    seed_data()
