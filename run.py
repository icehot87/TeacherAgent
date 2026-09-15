#!/usr/bin/env python3
"""
Akira's Teacher - Junior Kindergarten to Elementary AI Teacher Agent
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
    
    # Load .env file if present
    env_file = os.path.join(base_dir, ".env")
    if os.path.exists(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v
        except Exception:
            pass

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    # Discover local LAN IP
    local_ip = "localhost"
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    print("=" * 60)
    print("🌟 Akira's Teacher Portal is starting!")
    print(f"💻 On this device : http://localhost:{port}")
    if host == "0.0.0.0" and local_ip not in ("127.0.0.1", "localhost"):
        print(f"📱 Local Network : http://{local_ip}:{port}")
    print("🔒 Restricting to local network by default.")
    print("=" * 60)

    uvicorn.run("app.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    main()
