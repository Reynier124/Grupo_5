import os
import logging

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

from models.base_model import base

# Carga opcional del archivo .env (en caso de querer configurar la ruta de la DB vía .env)
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)

# Ruta de la base de datos SQLite (por defecto en la raíz del proyecto)
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "sqlite.db")

# URI de conexión para SQLite
DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"

logging.info(f"Using SQLite database at: {SQLITE_DB_PATH}")

class Database:
    _instance = None
    engine = create_engine(DATABASE_URI, connect_args={"check_same_thread": False})  # Necesario para SQLite en apps multihilo
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __init__(self):
        self._session = None
        self.create_tables_if_not_exist()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._engine = cls.engine
            cls._instance._SessionLocal = cls.SessionLocal
        return cls._instance

    def get_session(self) -> Session:
        if self._session is None:
            self._session = self._SessionLocal()
        return self._session

    def drop_database(self):
        try:
            base.metadata.drop_all(self._engine)
            print("Tables dropped.")
        except Exception as e:
            print(f"Error dropping tables: {e}")

    def create_tables(self):
        try:
            base.metadata.create_all(self._engine)
            print("Tables created.")
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    def create_tables_if_not_exist(self):
        inspector = inspect(self.engine)
        for table_name in base.metadata.tables.keys():
            if not inspector.has_table(table_name):
                try:
                    base.metadata.create_all(self.engine)
                    print(f"Table {table_name} created.")
                except Exception as e:
                    print(f"Error creating tables: {e}")
                break

    def close_session(self):
        if hasattr(self, "_session"):
            self._session.close()
            del self._session

    def check_connection(self):
        try:
            with self._engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Connection established.")
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
