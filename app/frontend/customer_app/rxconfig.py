"""
rxconfig.py contains the configuration for Reflex.
"""

import reflex as rx

prod_origins = ["http://127.0.0.1", "https://demo.bima-mo.com"]

dev_origins = ["*"]


config = rx.Config(
    app_name="customer_data",
    show_built_with_reflex=False,
    cors_allowed_origins=dev_origins,
    telemetry_enabled=False,
    backend_port=8001,
    frontend_port=3000,
    loglevel="debug",
    db_url=None,
    backend_host="127.0.0.1",
    gunicorn_worker_class="uvicorn.workers.UvicornH11Worker",
    gunicorn_workers=4,  # Set number of worker processes
    api_url="http://127.0.0.1:8001",
    is_reflex_cloud=False,
)
