#!/usr/bin/env python3
"""
启动后端服务的脚本
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

if __name__ == "__main__":
    import uvicorn

    os.chdir(SCRIPT_DIR)

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
