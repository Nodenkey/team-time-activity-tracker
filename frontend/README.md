# Frontend branch README

This branch adds a plain HTML/CSS/JS frontend for the Team Time Activity Tracker.

Key pieces:
- `frontend/index.html` – landing page with navigation and backend health indicator.
- `frontend/log.html` – time entry form wired to POST /entries.
- `frontend/list.html` – entries list with date/person filters using GET /entries.
- `frontend/css/styles.css` – shared layout and component styles.
- `frontend/js/*.js` – config and page-specific logic.
- `frontend/Dockerfile`, `frontend/railway.toml` – static nginx deployment setup.
