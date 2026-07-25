# Deploy to Streamlit Community Cloud

Quick steps to deploy the project to Streamlit Community Cloud.

1. Create a GitHub repository and push this project (root branch: `main` or `master`). Example commands:

```bash
git init
git add .
git commit -m "Initial commit - CrisisOps NovaRetail"
git branch -M main
git remote add origin https://github.com/<your-org-or-username>/<repo>.git
git push -u origin main
```

2. On Streamlit Community Cloud (https://share.streamlit.io) sign in with GitHub and click "New app".
   - Choose the GitHub repo, branch (`main`) and the app file path: `frontend/app.py`.
   - Click "Deploy".

3. Configure environment variables (App > Settings > Secrets) — add your secrets there. Typical env names used by this project:
   - `OPENAI_API_KEY` or `GEMINI_API_KEY` (LLM provider key)
   - `LANGSMITH_API_KEY` (LangSmith tracing)
   - `LANGGRAPH_API_KEY` (if used)
   - `CHROMA_SERVER_URL` or `CHROMA_DB_DIR` (if using remote Chroma)
   - `DATABASE_URL` (if you use a DB)
   - Any other keys from `.env` / `config/settings.py`

4. After deployment the app will run on Streamlit's Linux hosts (no Windows AppControl issues). Use the Streamlit UI to view logs and adjust settings.

Notes & troubleshooting
- If your app hangs during startup, check the "Logs" tab in Streamlit Cloud for missing packages or import errors.
- Large binary wheels (pyarrow, pandas, pyarrow) will be installed on deployment; Streamlit Cloud uses Linux wheels which avoid Windows Application Control problems.
- If you use large dependencies, Streamlit Cloud build can take several minutes.

Optional: automatic deploy on push
- In Streamlit Cloud app settings enable automatic deploys from the selected branch so each `git push` redeploys.

If you want, I can also scaffold a `Dockerfile` + GitHub Actions workflow instead (for Render/Cloud Run). Which do you prefer next?
