import os


def get_postgres_uri():
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    password = os.environ.get("DB_PASSWORD", "abc123")
    user, db_name = "flask-starter", "flask-starter"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
