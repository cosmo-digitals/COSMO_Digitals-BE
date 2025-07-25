from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.api.v1.endpoints.contact import router as contact_v1_router
from app.routes.contact import router as public_contact_router  # optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite dev server for admin panel
        "http://127.0.0.1:5173",  # Vite dev server for admin panel
        "http://localhost:8080",  # Alternative admin panel port
        "http://127.0.0.1:8080",  # Alternative admin panel port
        "*",  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _startup():
    await connect_to_mongo()


@app.on_event("shutdown")
async def _shutdown():
    await close_mongo_connection()


# register routes
app.include_router(contact_v1_router)
app.include_router(public_contact_router)  # remove if unused
