# FastAPI Social API

A learning project built while following the freeCodeCamp FastAPI course. It provides a REST API for user registration, authentication, posts, and votes, backed by PostgreSQL.

## Tech stack

Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic, and Docker.

## Run locally

1. Clone the repository and install the dependencies:

   ```bash
   git clone https://github.com/tabera2/fastapi.git
   cd fastapi
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a PostgreSQL database and a `.env` file in the project root. Set `DATABASE_HOSTNAME`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `SECRET_KEY`, `ALGORITHM` (for example, `HS256`), and `ACCESS_TOKEN_EXPIRE_MINUTES`. Keep credentials private and do not commit `.env`.

3. Apply the migrations and start the app:

   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

4. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API documentation. Create a user, then use **Authorize** with the user's email as the username and their password to access protected endpoints.

## API overview

- **Users and authentication:** register with `POST /users/`, retrieve a user with `GET /users/{id}`, and sign in with `POST /login`.
- **Posts:** create, list, retrieve, update, and delete posts through `/posts/`. Updates and deletions require ownership.
- **Votes:** use `POST /vote/` with `dir: 1` to add a vote or `dir: 0` to remove one.

The Dockerfile starts the API, but it does not automatically run database migrations. Apply migrations separately when deploying.
