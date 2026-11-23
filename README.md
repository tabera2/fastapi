# Creator Deals API demo

A FastAPI and PostgreSQL demo inspired by OVO Talent's creator campaign workflow. It adds a private deal tracker to the existing users, posts, votes, and login API. This is an independent demo, not an OVO product.

## What it does

Authenticated users can create, list, filter, view, update, and delete their own deals at `/deals/`. Each deal records a brand, creator, deliverables, a USD amount in cents, and a stage: `pitch`, `negotiation`, `brief`, `content_review`, `delivered`, or `paid`. Stages are labels and can be changed in any order. No payment, contract, notification, or real creator integration is implemented.

## Run locally

Use Python 3.12 and PostgreSQL. Install `requirements.txt`, configure the environment variables in `app/config.py` (use a local `.env` file, never commit credentials), run `alembic upgrade head`, and start `uvicorn app.main:app --reload`. Open `/docs`. Create a user with `POST /users/`, then use **Authorize** with the email as the username and password to log in.

## Two-minute demo

1. Open `/docs` and explain that the existing API now includes a creator-deals workflow.
2. Create a user and authorize with that account. Use fictitious data.
3. In `POST /deals/`, submit:

```json
{"brand":"Northstar Skincare","creator":"Alex Rivers","deliverables":"One Instagram Reel and two Stories","amount_cents":250000,"stage":"pitch"}
```

4. Explain that `250000` means $2,500 USD. Copy the returned deal ID. Use `PATCH /deals/{deal_id}` with `{"stage":"content_review"}` to show progress from pitch to content approval.
5. Use `GET /deals/` with `stage=content_review` to find the opportunity. Explain that deals are private to their owner and that the original posts and votes remain available.

Suggested close: “This prototype shows how I can extend an existing production-shaped API with a practical creator campaign workflow, validation, authorization, and database migrations.”

## Deployment preparation

The Dockerfile starts the web server but does **not** apply migrations. Before serving the new version, take a database backup, verify the existing Alembic revision and current Render configuration, and run `alembic upgrade head` once against the intended database in a controlled deployment step. Do not run destructive downgrades against production data. The new migration only adds a table and index; it does not modify existing records. A push to `main` may trigger an automatic Render deploy depending on service settings, so coordinate the migration and deployment. Keep all Render and database credentials in the service's secret configuration.

## Tests

Install `pytest` and `httpx` into the development environment, then run `python -m pytest -q`. Tests use a temporary in-memory database and cover deal lifecycle, account isolation, authentication, and validation. Production migrations should also be checked against PostgreSQL.
