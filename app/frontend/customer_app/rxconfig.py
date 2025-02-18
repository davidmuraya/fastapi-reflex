"""
rxconfig.py contains the configuration for Reflex.
"""

import reflex as rx

prod_origins = [
    "http://127.0.0.1",
]

dev_origins = ["*"]


config = rx.Config(
    app_name="customer_data",
    show_built_with_reflex=False,
    cors_allowed_origins=prod_origins,
    telemetry_enabled=False,
    backend_port=8000,
    frontend_port=3000,
    loglevel="debug",
    db_url=None,
    backend_host="127.0.0.1",
)
