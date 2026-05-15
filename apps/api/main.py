import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Aether Intelligence API",
    description="Enterprise-grade semantic codebase search and intelligence platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Aether Intelligence API",
        "version": "1.0.0",
        "capabilities": [
            "Semantic Search",
            "Graph Intelligence",
            "Autonomous Agents",
            "Architecture Analysis"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
