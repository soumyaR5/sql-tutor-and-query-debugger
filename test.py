from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:Soumya5@localhost:5432/sql_tutor"

engine = create_engine(DATABASE_URL)

conn = engine.connect()
print("✅ Connected from Python!")