# -*- coding: utf-8 -*-
"""
===================================
Daily Stock Analysis - FastAPI Backend Entry Point
===================================

Responsibilities:
1. Provide the RESTful API service
2. Configure CORS support
3. Provide a health check endpoint
4. Serve frontend static files (production mode)

How to start:
    uvicorn server:app --reload --host 0.0.0.0 --port 8000
    
    Or use main.py:
    python main.py --serve-only      # Start the API service only
    python main.py --serve           # API service + run analysis
"""

import logging

from ai_stock.config import setup_env, get_config
from ai_stock.logging_config import setup_logging

# Import the application instance from api.app
from api.app import app  # noqa: E402

# Initialize environment variables and logging
setup_env()

CONFIG = get_config()
level_name = (CONFIG.log_level or "INFO").upper()
level = getattr(logging, level_name, logging.INFO)

setup_logging(
    log_prefix="api_server",
    console_level=level,
    extra_quiet_loggers=['uvicorn', 'fastapi'],
)

# Export app for use by uvicorn
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
