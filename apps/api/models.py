from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    branch = Column(String, default="main")
    status = Column(String, default="pending")  # pending, indexing, indexed, error
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_indexed_at = Column(DateTime)
    
    files = relationship("File", back_populates="repository", cascade="all, delete-orphan")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    repo_id = Column(String, ForeignKey("repositories.id"))
    path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    extension = Column(String)
    size = Column(Integer)
    content_hash = Column(String)
    last_modified = Column(DateTime)
    
    repository = relationship("Repository", back_populates="files")
    symbols = relationship("Symbol", back_populates="file", cascade="all, delete-orphan")

class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    name = Column(String, nullable=False)
    type = Column(String)  # function, class, method, etc.
    start_line = Column(Integer)
    end_line = Column(Integer)
    
    file = relationship("File", back_populates="symbols")

class IndexTask(Base):
    __tablename__ = "index_tasks"

    id = Column(String, primary_key=True)
    repo_id = Column(String, ForeignKey("repositories.id"))
    status = Column(String)  # queued, processing, completed, failed
    progress = Column(Integer, default=0)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow)
