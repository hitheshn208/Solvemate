from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from taylor_series import router as taylor_router
from newton_raphson import router as newton_router 
from newton_raphson_2_var import router as newton2_router
from taylor2 import router as taylor2_router
from euler import router as euler_router
from modified_euler import router as modified_euler_router
from rk4 import router as rk4_router




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
@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return Response(status_code=204)

# Include Taylor series API router
app.include_router(taylor_router)
# Include Newton Raphson API router
app.include_router(newton_router)

# Include Newton Raphson for 2 variable API router
app.include_router(newton2_router)

# Include Taylor series for 2 variable API router
app.include_router(taylor2_router)

# Include Euler method API router
app.include_router(euler_router)

# Include Modified Euler method API router
app.include_router(modified_euler_router)

# Include Runge-Kutta method API router
app.include_router(rk4_router)