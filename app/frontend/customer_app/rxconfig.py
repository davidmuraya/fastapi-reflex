"""
rxconfig.py contains the configuration for Reflex.
"""

import reflex as rx

prod_origins = [
    "http://localhost",
    "http://127.0.0.1",
]

dev_origins = ["*"]


config = rx.Config(
    app_name="customer_data",
    show_built_with_reflex=False,
    cors_allowed_origins=dev_origins,
    backend_port=8000,
    frontend_port=3000,
)
