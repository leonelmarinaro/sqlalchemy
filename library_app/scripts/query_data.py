from library_app.db import SessionLocal
from library_app.models.user import Author, Book


def query_data():
    db = SessionLocal()

    print("\n--- Autores ---")
    authors = db.query(Author).all()
    for author in authors:
        print(f"ID: {author.id}, Nombre: {author.name}")
        print(f"Libros: {len(author.books)}")

    print("\n--- Libros ---")
    books = db.query(Book).all()
    for book in books:
        print(f"ID: {book.id}, Título: {book.title}")
        print(f"Autor: {book.author.name}")
        print(f"Disponible: {'Sí' if book.is_available else 'No'}")
        print("---")

    db.close()


if __name__ == "__main__":
    query_data()
