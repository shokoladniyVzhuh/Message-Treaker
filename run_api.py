#!/usr/bin/env python3
"""
Message Treaker API Runner
Запуск FastAPI сервера
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from watcher.settings import API_HOST, API_PORT

if __name__ == "__main__":
    print(f"🌐 Starting Message Treaker API on {API_HOST}:{API_PORT}")
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)



