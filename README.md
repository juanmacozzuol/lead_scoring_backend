# Lead Scoring Backend

Backend API for a lead scoring system, built with FastAPI and MySQL. This is my final capstone project for a Systems Analyst degree, developed together with a teammate who built the frontend: [lead_scoring_frontend](https://github.com/Beraldocamila/lead_scoring_frontend).

## Stack

- **FastAPI**
- **SQLAlchemy** + **Alembic** (migrations)
- **MySQL** (via PyMySQL)

## Running it locally

1. Create an empty MySQL database named `lead_scoring`.
2. Create a `.env` file in the root with your database connection string:

   ```
   DATABASE_URL=mysql+pymysql://user:password@host:port/lead_scoring
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. Check the database connection at `http://127.0.0.1:8000/probandoDB` — a healthy response looks like:

   ```json
   {"db_status": "ok"}
   ```
