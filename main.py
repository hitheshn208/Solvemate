from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from taylor_series import router as taylor_router  # your router file
from newton_raphson import router as newton_router #router file for newton raphson
from newton_raphson_2_var import router as newton2_router



app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing. Restrict later if needed.
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve HTML frontend
@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

# Hidden health check route for UptimeRobot
@app.get("/health")
def health_check():
    return Response(status_code=204)

# Include Taylor series API router
app.include_router(taylor_router)
# Include Newton Raphson API router
app.include_router(newton_router)

# Include Newton Raphson for 2 variable API router
app.include_router(newton2_router)