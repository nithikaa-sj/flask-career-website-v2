from sqlalchemy import create_engine, engine,text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string)

def load_jobs_from_db():
  with engine.connect() as conn:
      result = conn.execute(text("select * from jobs"))

      jobs = []
      for row in result.mappings():
          jobs.append(dict(row))

      return jobs
