from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taylor_series import router as taylor_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(taylor_router)
