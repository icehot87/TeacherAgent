#!/usr/bin/env python3
"""
Teacher Spark - Junior Kindergarten to Elementary AI Teacher Agent
Launcher script
"""
import os
import sys
import uvicorn

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    # Ensure directories exist
    os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "uploads"), exist_ok=True)
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"🌟 Starting Teacher Spark Portal on http://localhost:{port} ...")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
