# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Scope

This file covers `niffler-e-2-e-tests-python`, the Python E2E test suite for the Niffler project (a
multi-service Java/React app; see the repo root `README.md` for the full system). This suite drives the
Niffler frontend through a browser (Selene/Selenium), calls the `niffler-spend` service via its HTTP
gateway, and reads/writes the `niffler-spend` Postgres database directly for setup/teardown.

## Setup

Dependencies are in `requirements.txt` (no `pyproject.toml`/`setup.cfg` — plain pip):

```bash
pip install -r requirements.txt
```

Configuration is via a `.env` file in this directory (see `.env.sample` for the required keys):

- `FRONTEND_URL` — Niffler frontend base URL (e.g. `http://frontend.niffler.dc`)
- `GATEWAY_URL` — API gateway base URL (e.g. `http://gateway.niffler.dc:8090`)
- `SPEND_DB_URL` — SQLAlchemy URL for the `niffler-spend` Postgres DB
- `TEST_USERNAME` / `TEST_PASSWORD` — credentials for the test user used to log in

These match the local-dev topology described in the root `README.md` (Docker-based Postgres, `/etc/hosts`
aliases for `*.niffler.dc`, services started via `docker-compose-dev.sh` or run individually in the IDE).
The frontend must be reachable and logged in via its real auth flow — there is no API-based login shortcut.

## Running tests

```bash
pytest
pytest tests/test_spending.py::test_spending_title_exists   # single test
pytest -m <marker>                                          # if/when markers are added
pytest --alluredir=allure-results                           # allure results (already gitignored)
```

Tests drive a real browser via Selene, so a display/webdriver (or a Selenoid-style remote grid, per the
root README) must be available. `allure-results/` and `__pycache__/` are generated output — do not edit
them by hand.

## Architecture

The suite is a thin layer over three collaborators, wired together by fixtures in `conftest.py`:

- **`clients/spends_client.py`** — `SpendsHttpClient`, a `requests`-based client for the spend service's
  REST API (via the gateway), authenticated with a bearer token. Used for fast, UI-independent
  setup/teardown of spends and categories (`add_spends`, `remove_spends`, `add_category`,
  `get_categories`, `get_spends`).
- **`databases/spend_db.py`** — `SpendDb`, a SQLModel/SQLAlchemy wrapper around the `niffler-spend`
  Postgres DB, used to clean up state the HTTP API can't reach directly (e.g. `delete_category`).
- **`models/`** — Pydantic/SQLModel schemas shared by the client and DB layers: `spend.py` defines
  `Category` and `Spend` (SQLModel table models, also used as API response schemas) and `SpendAdd` (a
  plain Pydantic request model); `config.py` defines `Envs`, the typed view of the `.env` config.

`conftest.py` fixtures build the object graph and manage test data lifecycle:

- `envs` (session) loads `.env` into an `Envs` instance.
- `auth` (session) drives the real login flow in the browser (Selene) and extracts the `id_token` from
  `sessionStorage` — this is the bearer token used everywhere else, so any UI change to the login form
  breaks every authenticated fixture, not just UI tests.
- `spends_client` / `spend_db` (session) are built from `envs`/`auth`.
- `spends` and `category` are **parametrized, indirect** fixtures (`params=[]` by default) that create
  data via the API before the test and tear it down after — even if the test itself deletes/mutates the
  data (`spends` checks the spend still exists before trying to remove it). Tests select the actual data
  via `marks.py`'s `TestData.spends(...)` / `TestData.category(...)`, which wrap
  `pytest.mark.parametrize(..., indirect=True)`.
- `main_page` opens the frontend after auth; `main_page_late` (in `test_spending.py`) additionally waits
  for `category`/`spends` to be created first, so the page loads with that data already present.

`marks.py` centralizes reusable marker helpers instead of repeating `pytest.mark.usefixtures`/
`parametrize` boilerplate: `Pages.main_page` for tests needing the logged-in main page, and
`TestData.category(...)` / `TestData.spends(...)` for tests needing specific pre-seeded data (Spend IDs
are exposed via `.description` for readable test IDs).

When adding a new test that needs seeded data, prefer extending the `spends`/`category` fixtures' pattern
(API-created, API/DB-torn-down) over creating data through the UI.
