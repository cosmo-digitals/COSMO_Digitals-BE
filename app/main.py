# app/main.py
from fastapi import FastAPI
from app.database.mongodb import connect_to_mongo, close_mongo_connection
from app.routes.contact import router as contact_router
from fastapi.middleware.cors import CORSMiddleware
    
app = FastAPI()
 
 # Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://127.0.0.1:3000",],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# MongoDB connection handling
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Register all routes
app.include_router(contact_router)
 
 

# from fastapi import FastAPI
# from app.database.mongodb import connect_to_mongo, close_mongo_connection
# from app.routes.contact import router as contact_router
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # Allow frontend to access API
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Connect to MongoDB at startup
# @app.on_event("startup")
# async def startup_event():
#     await connect_to_mongo()

# # Disconnect on shutdown
# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_mongo_connection()

# # Mount the contact form routes
# app.include_router(contact_router)
