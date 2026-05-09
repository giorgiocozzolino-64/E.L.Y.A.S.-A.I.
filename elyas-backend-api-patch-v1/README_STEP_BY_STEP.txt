E.L.Y.A.S.-A.I. Backend API Patch v1

GOAL
Fix current frontend 404 errors:
/api/v1/casks
/api/v1/portfolio/summary

INSTALL
1. Upload app/elyas_api_routes.py into:
   elyas-backend-v1/app/elyas_api_routes.py

2. Open:
   app/main.py

3. Add:
   from app.elyas_api_routes import router as elyas_api_router
   app.include_router(elyas_api_router, prefix="/api/v1")

4. Redeploy Railway.

TEST AFTER DEPLOY
https://elyas-ai-production.up.railway.app/api/v1/health
https://elyas-ai-production.up.railway.app/api/v1/casks
https://elyas-ai-production.up.railway.app/api/v1/portfolio/summary
https://elyas-ai-production.up.railway.app/api/v1/dashboard/investor
https://elyas-ai-production.up.railway.app/api/v1/netsuite/status

EXPECTED RESULT
JSON data, no 404.
