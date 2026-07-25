# Deployment Checklist

## ✅ Completed
- `streamlit.toml` — Cloud config ready
- `.github/workflows/ci.yml` — Tests run on push automatically
- `.gitignore` — Excludes .venv, __pycache__, .env, data/*.db
- `README_DEPLOY_STREAMLIT.md` — Full deployment guide
- Project code & tests (4 passing)

## 📋 Your Next Steps (3 commands)

### Step 1: Initialize git
```bash
cd C:\Users\danthuluri.varma\Desktop\GlobalLogic_Training\Project
git init
git add .
git commit -m "CrisisOps NovaRetail AI - ready for Streamlit Cloud"
```

### Step 2: Create GitHub repo (you do this once)
- Go to https://github.com/new
- Create a repo named `crisisops-novaretail` (or your choice)
- **Copy the repo URL** (e.g., `https://github.com/yourname/crisisops-novaretail.git`)

### Step 3: Push to GitHub
```bash
git branch -M main
git remote add origin <PASTE_YOUR_REPO_URL_HERE>
git push -u origin main
```

## 🚀 Then: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repo → branch `main` → file `frontend/app.py`
4. Click "Deploy"
5. After it launches, go to **Settings → Secrets** and add these env vars (get from your `.env` file):
   - `OPENAI_API_KEY` or `GEMINI_API_KEY`
   - `LANGSMITH_API_KEY`
   - Any other keys from `config/settings.py`

Done! Your app will run in the cloud on Linux (no Windows DLL issues).

---

**Questions?** See [README_DEPLOY_STREAMLIT.md](README_DEPLOY_STREAMLIT.md) for detailed troubleshooting.
