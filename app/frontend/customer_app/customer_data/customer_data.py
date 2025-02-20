"""
Customer data app.
"""

import reflex as rx

from .pages.contact import contact_page
from .pages.dashboard import dashboard_page
from .pages.login import login_page

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="large",
        accent_color="grass",
        scaling="90%",
    ),
)
