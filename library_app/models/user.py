from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# Reemplaza la importación relativa con una absoluta
import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from library_app.db import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con los libros
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author {self.name}>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    publication_year = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación con el autor
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"
